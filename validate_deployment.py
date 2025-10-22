#!/usr/bin/env python3
"""
Vercel Deployment Validator
验证 Vercel 部署所需的文件和配置
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath, required=True):
    """Check if a file exists"""
    exists = Path(filepath).exists()
    status = "✅" if exists else ("❌" if required else "⚠️")
    req_text = "Required" if required else "Optional"
    print(f"{status} {filepath} ({req_text})")
    return exists

def check_vercel_deployment():
    """Validate Vercel deployment setup"""
    print("=" * 70)
    print("🔍 Vercel Deployment Validator")
    print("=" * 70)
    print()
    
    all_good = True
    
    # Check required files
    print("📁 Checking required files...")
    required_files = [
        'vercel.json',
        'requirements.txt',
        'api/index.py',
        'app.py',
        'config.py',
    ]
    
    for file in required_files:
        if not check_file_exists(file, required=True):
            all_good = False
    
    print()
    
    # Check optional files
    print("📄 Checking optional files...")
    optional_files = [
        '.vercelignore',
        'runtime.txt',
        '.env.example',
        'VERCEL_DEPLOYMENT.md',
    ]
    
    for file in optional_files:
        check_file_exists(file, required=False)
    
    print()
    
    # Check vercel.json content
    print("⚙️ Checking vercel.json configuration...")
    try:
        import json
        with open('vercel.json', 'r') as f:
            config = json.load(f)
            
        checks = {
            'version': config.get('version') == 2,
            'builds': 'builds' in config and len(config['builds']) > 0,
            'routes': 'routes' in config and len(config['routes']) > 0,
        }
        
        for check, passed in checks.items():
            status = "✅" if passed else "❌"
            print(f"{status} {check}: {passed}")
            if not passed:
                all_good = False
    except Exception as e:
        print(f"❌ Error reading vercel.json: {e}")
        all_good = False
    
    print()
    
    # Check requirements.txt
    print("📦 Checking requirements.txt...")
    try:
        with open('requirements.txt', 'r') as f:
            requirements = f.read()
            
        required_packages = ['Flask', 'pymongo', 'python-dotenv']
        for package in required_packages:
            if package.lower() in requirements.lower():
                print(f"✅ {package} found")
            else:
                print(f"❌ {package} missing")
                all_good = False
    except Exception as e:
        print(f"❌ Error reading requirements.txt: {e}")
        all_good = False
    
    print()
    
    # Check environment variables
    print("🔐 Environment variables to configure in Vercel Dashboard...")
    env_vars = [
        ('SECRET_KEY', 'Flask session secret key'),
        ('FLASK_ENV', 'Set to "production"'),
        ('MONGODB_URI', 'MongoDB Atlas connection string'),
        ('OPENAI_API_KEY', 'OpenAI or GitHub PAT (for AI features)'),
        ('OPENAI_MODEL', 'AI model name (e.g., gpt-4o-mini)'),
    ]
    
    print("\nRequired environment variables:")
    for var, desc in env_vars:
        print(f"  • {var}: {desc}")
    
    print()
    
    # Final summary
    print("=" * 70)
    if all_good:
        print("✅ All checks passed! Ready for Vercel deployment.")
        print()
        print("Next steps:")
        print("1. Commit and push all changes to GitHub")
        print("2. Go to https://vercel.com and import your repository")
        print("3. Configure environment variables in Vercel Dashboard")
        print("4. Deploy!")
        print()
        print("📖 See VERCEL_DEPLOYMENT.md for detailed instructions")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("📖 See VERCEL_DEPLOYMENT.md for help")
    print("=" * 70)
    
    return all_good

if __name__ == '__main__':
    try:
        success = check_vercel_deployment()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
