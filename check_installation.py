#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para verificar la instalación de Neuro UX Styler
"""

import os
import sys

def check_file(filepath, description):
    """Verifica si un archivo existe"""
    exists = os.path.exists(filepath)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {filepath}")
    return exists

def check_directory(dirpath, description):
    """Verifica si un directorio existe"""
    exists = os.path.isdir(dirpath)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {dirpath}")
    return exists

def check_dependencies():
    """Verifica las dependencias de Python"""
    print("\n📦 Verificando dependencias de Python...")
    dependencies = [
        ('flask', 'Flask'),
        ('flask_cors', 'Flask-CORS'),
        ('tensorflow', 'TensorFlow'),
        ('numpy', 'NumPy'),
        ('pandas', 'Pandas'),
        ('sklearn', 'Scikit-learn'),
        ('joblib', 'Joblib')
    ]
    
    all_ok = True
    for module, name in dependencies:
        try:
            __import__(module)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} - NO INSTALADO")
            all_ok = False
    
    return all_ok

def main():
    print("=" * 60)
    print("🧠 NEURO UX STYLER - VERIFICACIÓN DE INSTALACIÓN")
    print("=" * 60)
    
    # Verificar estructura de directorios
    print("\n📁 Verificando estructura de directorios...")
    dirs_ok = all([
        check_directory('backend', 'Backend'),
        check_directory('backend/data', 'Data'),
        check_directory('backend/data/models', 'Models'),
    ])
    
    # Verificar archivos backend
    print("\n📄 Verificando archivos del backend...")
    backend_ok = all([
        check_file('backend/requirements.txt', 'Requirements'),
        check_file('backend/app.py', 'API Flask'),
        check_file('backend/model.py', 'Modelo'),
        check_file('backend/training.py', 'Training'),
        check_file('backend/data_processor.py', 'Data Processor'),
        check_file('backend/data/training_data.json', 'Training Data'),
    ])
    
    # Verificar archivos frontend
    print("\n🌐 Verificando archivos del frontend...")
    frontend_ok = check_file('index.html', 'HTML Principal')
    
    # Opcional: archivos separados
    has_separate_files = all([
        os.path.exists('styles.css'),
        os.path.exists('app.js')
    ])
    
    if has_separate_files:
        print("ℹ️  Archivos CSS/JS separados detectados")
    
    # Verificar modelo entrenado
    print("\n🤖 Verificando modelo...")
    model_exists = check_file('backend/data/models/neuro_ux_model.h5', 'Modelo entrenado')
    if not model_exists:
        print("⚠️  Modelo no encontrado. Necesitas ejecutar: python backend/training.py")
    
    # Verificar dependencias
    deps_ok = check_dependencies()
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN")
    print("=" * 60)
    
    if dirs_ok and backend_ok and frontend_ok and deps_ok:
        print("✅ Todo está correctamente instalado!")
        print("\n🚀 PRÓXIMOS PASOS:")
        if not model_exists:
            print("   1. Entrenar el modelo:")
            print("      cd backend && python training.py")
            print("   2. Iniciar el servidor:")
            print("      python app.py")
            print("   3. Abrir index.html en tu navegador")
        else:
            print("   1. Iniciar el servidor:")
            print("      cd backend && python app.py")
            print("   2. Abrir index.html en tu navegador")
    else:
        print("❌ Hay problemas en la instalación")
        print("\n🔧 PROBLEMAS DETECTADOS:")
        if not dirs_ok:
            print("   - Faltan directorios")
        if not backend_ok:
            print("   - Faltan archivos del backend")
        if not frontend_ok:
            print("   - Falta el archivo HTML")
        if not deps_ok:
            print("   - Faltan dependencias de Python")
            print("     Ejecuta: pip install -r backend/requirements.txt")
    
    print("=" * 60)

if __name__ == "__main__":
    main()