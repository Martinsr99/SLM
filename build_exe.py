"""
Build script for creating AutoVolumeManager executable
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("[INFO] PyInstaller is already installed")
    except ImportError:
        print("[INFO] Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("[INFO] PyInstaller installed successfully")

def create_spec_file():
    """Create PyInstaller spec file for better control"""
    spec_content = '''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config.template.json', '.'),
        ('README.md', '.'),
    ],
    hiddenimports=[
        'customtkinter',
        'pycaw',
        'comtypes',
        'src.config.settings',
        'src.config.languages',
        'src.core.audio_utils',
        'src.core.volume_manager',
        'src.ui.main_window',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AutoVolumeManager',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Set to False to hide console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path here if you have one
)
'''
    
    with open('AutoVolumeManager.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content.strip())
    
    print("[INFO] Created AutoVolumeManager.spec file")

def build_executable():
    """Build the executable using PyInstaller"""
    print("[INFO] Building executable...")
    
    # Clean previous builds
    if os.path.exists('dist'):
        shutil.rmtree('dist')
        print("[INFO] Cleaned previous dist directory")
    
    if os.path.exists('build'):
        shutil.rmtree('build')
        print("[INFO] Cleaned previous build directory")
    
    # Build using spec file
    cmd = [sys.executable, "-m", "PyInstaller", "--clean", "AutoVolumeManager.spec"]
    
    try:
        subprocess.check_call(cmd)
        print("[INFO] Build completed successfully!")
        
        # Check if executable was created
        exe_path = Path("dist/AutoVolumeManager.exe")
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"[INFO] Executable created: {exe_path}")
            print(f"[INFO] File size: {size_mb:.1f} MB")
            
            # Copy config template to dist folder
            if os.path.exists('config.template.json'):
                shutil.copy2('config.template.json', 'dist/')
                print("[INFO] Copied config template to dist folder")
            
            return True
        else:
            print("[ERROR] Executable not found after build")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Build failed: {e}")
        return False

def create_simple_build():
    """Create a simple one-file executable"""
    print("[INFO] Creating simple one-file executable...")
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",  # Remove this line if you want to see console
        "--name", "AutoVolumeManager",
        "--add-data", "config.template.json;.",
        "--hidden-import", "customtkinter",
        "--hidden-import", "pycaw",
        "--hidden-import", "comtypes",
        "main.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("[INFO] Simple build completed!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Simple build failed: {e}")
        return False

def main():
    """Main build function"""
    print("AutoVolumeManager Executable Builder")
    print("=" * 40)
    
    # Install PyInstaller
    install_pyinstaller()
    
    print("\nChoose build method:")
    print("1. Advanced build with spec file (recommended)")
    print("2. Simple one-file build")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        create_spec_file()
        success = build_executable()
    elif choice == "2":
        success = create_simple_build()
    else:
        print("[ERROR] Invalid choice")
        return
    
    if success:
        print("\n" + "=" * 40)
        print("[SUCCESS] Executable build completed!")
        print("Check the 'dist' folder for your executable.")
        print("\nTo distribute your application:")
        print("1. Copy the entire 'dist' folder")
        print("2. Or just the .exe file if using one-file build")
        print("3. Include config.template.json for users")
    else:
        print("\n[ERROR] Build failed. Check the error messages above.")

if __name__ == "__main__":
    main()
