"""
Kraftbeat Device Detection Module

Provides automatic GPU/CPU backend detection with DirectML as primary target.
Supports: DirectML (AMD/Intel Windows), CUDA (NVIDIA), MPS (Apple), CPU (fallback)
"""

import logging
from enum import Enum
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


class DeviceType(Enum):
    """Supported compute device types."""
    DIRECTML = "directml"
    CUDA = "cuda"
    ROCM = "rocm"
    ZLUDA = "zluda"
    MPS = "mps"
    CPU = "cpu"


class DeviceInfo:
    """Information about the selected compute device."""
    
    def __init__(self, device_type: DeviceType, device_name: str, device_obj):
        self.device_type = device_type
        self.device_name = device_name
        self.device_obj = device_obj  # The actual torch device object
    
    def __str__(self):
        return f"{self.device_type.value}: {self.device_name}"
    
    @property
    def is_gpu(self) -> bool:
        return self.device_type != DeviceType.CPU


def detect_directml() -> Optional[Tuple[str, object]]:
    """Try to detect DirectML device (AMD/Intel on Windows).
    
    Prefers discrete GPUs over integrated GPUs when multiple are available.
    """
    try:
        import torch_directml
        
        # Get number of available DirectML devices
        device_count = torch_directml.device_count()
        logger.info(f"DirectML: Found {device_count} device(s)")
        
        if device_count == 0:
            return None
        
        # Enumerate all devices to find the best one
        best_device_idx = 0
        best_device_name = torch_directml.device_name(0)
        
        for i in range(device_count):
            name = torch_directml.device_name(i)
            logger.info(f"  Device {i}: {name}")
            
            # Prefer discrete GPUs (RX, RTX, GTX, Arc) over integrated
            # Integrated GPUs often have generic names like "AMD Radeon(TM) Graphics"
            is_discrete = any(keyword in name.upper() for keyword in [
                'RX ', 'RTX ', 'GTX ', 'ARC ', 
                'RADEON RX', 'GEFORCE', 'NAVI', 
                '6600', '6700', '6800', '6900',  # AMD RX 6000 series
                '7600', '7700', '7800', '7900',  # AMD RX 7000 series
            ])
            
            is_integrated = any(keyword in name.upper() for keyword in [
                'RADEON(TM) GRAPHICS',  # AMD APU iGPU
                'INTEL UHD', 'INTEL IRIS',  # Intel iGPU
                'VEGA', 'RAPHAEL',  # AMD APU names
            ])
            
            # Prefer discrete over integrated
            current_is_discrete = any(keyword in best_device_name.upper() for keyword in [
                'RX ', 'RTX ', 'GTX ', 'ARC ',
            ])
            
            if is_discrete and not current_is_discrete:
                best_device_idx = i
                best_device_name = name
                logger.info(f"  -> Preferring discrete GPU: {name}")
            elif not is_integrated and i > 0 and 'RADEON(TM) GRAPHICS' in best_device_name.upper():
                # If current best is iGPU and this one isn't clearly integrated, prefer this one
                best_device_idx = i
                best_device_name = name
                logger.info(f"  -> Preferring non-integrated: {name}")
        
        device = torch_directml.device(best_device_idx)
        logger.info(f"DirectML selected: {best_device_name} (device {best_device_idx})")
        return best_device_name, device
        
    except ImportError:
        logger.debug("torch-directml not installed")
        return None
    except Exception as e:
        logger.warning(f"DirectML detection failed: {e}")
        return None


def detect_cuda() -> Optional[Tuple[str, object]]:
    """Try to detect generic CUDA device (NVIDIA)."""
    try:
        import torch
        if torch.cuda.is_available():
            device = torch.device("cuda")
            device_name = torch.cuda.get_device_name(0)
            
            # Filter out if it's actually ZLUDA masquerading (if we can tell)
            # Usually ZLUDA just looks like CUDA, so we trust it unless we seek ZLUDA explicitly
            logger.info(f"CUDA detected: {device_name}")
            return device_name, device
    except ImportError:
        logger.debug("torch not installed")
        return None
    except Exception as e:
        logger.warning(f"CUDA detection failed: {e}")
        return None
    return None


def detect_rocm() -> Optional[Tuple[str, object]]:
    """Try to detect ROCm device (AMD Native - Linux or Windows with ROCm PyTorch).
    
    ROCm on Windows (Preview):
    - Requires ROCm 6.4+ with Windows PyTorch support
    - Supports RX 7000/9000 series (RDNA 3/4)
    - Supports Ryzen AI 300/AI Max APUs
    """
    try:
        import torch
        
        # Check for HIP (ROCm's CUDA-like API)
        has_hip = hasattr(torch.version, 'hip') and torch.version.hip is not None
        
        if has_hip and torch.cuda.is_available():
            device = torch.device("cuda")
            device_name = torch.cuda.get_device_name(0)
            hip_version = torch.version.hip if torch.version.hip else "unknown"
            logger.info(f"ROCm detected (HIP {hip_version}): {device_name}")
            return device_name, device
        
        # Alternative detection: Check for AMD in device name when using ROCm wheels
        if torch.cuda.is_available():
            device_name = torch.cuda.get_device_name(0).lower()
            # AMD devices on ROCm often have 'gfx' or 'amd' in their name
            if 'gfx' in device_name or 'amd' in device_name or 'radeon' in device_name:
                device = torch.device("cuda")
                real_name = torch.cuda.get_device_name(0)
                logger.info(f"ROCm detected (AMD GPU): {real_name}")
                return real_name, device
                
    except ImportError as e:
        logger.debug(f"ROCm detection: torch could not be imported: {e}")
    except AttributeError as e:
        # torch.version.hip might not exist in standard PyTorch builds
        logger.debug(f"ROCm detection: torch has no version.hip: {e}")
    except Exception as e:
        logger.warning(f"ROCm detection failed: {e}")
    return None


def detect_zluda() -> Optional[Tuple[str, object]]:
    """Try to detect ZLUDA (AMD->CUDA translation)."""
    # ZLUDA makes AMD GPUs look like CUDA.
    # Often we just use normal CUDA detection, but if we want to be explicit:
    try:
        import torch
        import os
        # If user explicitly wants ZLUDA, we check if standard CUDA works
        # and maybe check environment variables specific to ZLUDA if they exist
        if torch.cuda.is_available():
            # ZLUDA often renames the device or we can assume it's ZLUDA if
            # we are on Windows+AMD but CUDA works (and no DirectML force).
            device = torch.device("cuda")
            device_name = torch.cuda.get_device_name(0)
            logger.info(f"ZLUDA/CUDA detected: {device_name}")
            return device_name, device
    except Exception as e:
        logger.warning(f"ZLUDA detection failed: {e}")
    return None


def detect_mps() -> Optional[Tuple[str, object]]:
    """Try to detect MPS device (Apple Silicon)."""
    try:
        import torch
        if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            device = torch.device("mps")
            logger.info("MPS (Apple Silicon) detected")
            return "Apple Silicon", device
    except ImportError:
        logger.debug("torch not installed")
        return None
    except Exception as e:
        logger.warning(f"MPS detection failed: {e}")
        return None
    return None


def get_cpu_device() -> Tuple[str, object]:
    """Get CPU device as fallback."""
    import torch
    return "CPU", torch.device("cpu")


def get_device(preferred: Optional[DeviceType] = None) -> DeviceInfo:
    """
    Detect and return the best available compute device.
    
    Priority order (unless preferred is specified):
    1. DirectML (AMD/Intel on Windows) - primary dev target
    2. CUDA (NVIDIA)
    3. MPS (Apple Silicon)
    4. CPU (fallback)
    
    Args:
        preferred: Optional preferred device type to try first
        
    Returns:
        DeviceInfo with the selected device
    """
    # Unified detection order (priority: DirectML > CUDA > ZLUDA > ROCm > MPS)
    detection_order = [
        (DeviceType.DIRECTML, detect_directml),
        (DeviceType.CUDA, detect_cuda),
        (DeviceType.ZLUDA, detect_zluda),
        (DeviceType.ROCM, detect_rocm),
        (DeviceType.MPS, detect_mps),
    ]
    
    # If preferred is CPU, return immediately
    if preferred == DeviceType.CPU:
        logger.info("Preferred device is CPU")
        cpu_name, cpu_device = get_cpu_device()
        return DeviceInfo(DeviceType.CPU, cpu_name, cpu_device)
        
    # If preferred device specified (and not CPU), try it first
    if preferred:
        for device_type, detector in detection_order:
            if device_type == preferred:
                result = detector()
                if result:
                    return DeviceInfo(device_type, result[0], result[1])
                logger.warning(f"Preferred device {preferred.value} not available")
    
    # Try each device in priority order
    for device_type, detector in detection_order:
        result = detector()
        if result:
            return DeviceInfo(device_type, result[0], result[1])
    
    # Fallback to CPU
    logger.info("No GPU detected, using CPU")
    cpu_name, cpu_device = get_cpu_device()
    return DeviceInfo(DeviceType.CPU, cpu_name, cpu_device)


def print_device_info():
    """Print detected device information to console."""
    device = get_device()
    logger.info("╔══════════════════════════════════════╗")
    logger.info("║  Kraftbeat Device Detection          ║")
    logger.info("╠══════════════════════════════════════╣")
    logger.info(f"║  Backend: {device.device_type.value.upper():<24}  ║")
    logger.info(f"║  Device:  {device.device_name[:24]:<24}  ║")
    logger.info(f"║  GPU:     {'Yes' if device.is_gpu else 'No':<24}  ║")
    logger.info("╚══════════════════════════════════════╝")
    return device


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print_device_info()
