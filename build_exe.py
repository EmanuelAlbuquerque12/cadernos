#!/usr/bin/env python3
"""
Script para criar o executável (.exe) do Baixador de Cadernos PJe
"""

import os
import sys
import shutil
import subprocess


def verificar_pyinstaller():
    """Verifica se PyInstaller está instalado"""
    try:
        import PyInstaller
        print("✓ PyInstaller encontrado")
        return True
    except ImportError:
        print("❌ PyInstaller não encontrado!")
        print("   Instalando PyInstaller...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
            print("✓ PyInstaller instalado com sucesso")
            return True
        except:
            print("❌ Erro ao instalar PyInstaller")
            return False


def verificar_dependencias():
    """Verifica se todas as dependências estão instaladas"""
    print("\nVerificando dependências...")

    dependencias = ['flask', 'requests', 'PyPDF2', 'urllib3']
    faltando = []

    for dep in dependencias:
        try:
            __import__(dep.lower())
            print(f"  ✓ {dep}")
        except ImportError:
            print(f"  ❌ {dep}")
            faltando.append(dep)

    if faltando:
        print(f"\n⚠️  Dependências faltando: {', '.join(faltando)}")
        print("   Instalando dependências...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
            print("✓ Dependências instaladas")
        except:
            print("❌ Erro ao instalar dependências")
            return False

    return True


def limpar_builds_antigos():
    """Remove builds anteriores"""
    print("\nLimpando builds antigos...")

    dirs_para_remover = ['build', 'dist', '__pycache__']

    for dir_name in dirs_para_remover:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"  ✓ Removido: {dir_name}")
            except Exception as e:
                print(f"  ⚠️  Erro ao remover {dir_name}: {e}")


def criar_executavel():
    """Cria o executável usando PyInstaller"""
    print("\n" + "=" * 60)
    print("Criando executável...")
    print("=" * 60)

    # Comando PyInstaller
    cmd = [
        'pyinstaller',
        '--clean',
        '--noconfirm',
        'BaixadorCadernosPJe.spec'
    ]

    try:
        subprocess.check_call(cmd)
        print("\n" + "=" * 60)
        print("✅ Executável criado com sucesso!")
        print("=" * 60)
        return True
    except subprocess.CalledProcessError as e:
        print("\n" + "=" * 60)
        print("❌ Erro ao criar executável!")
        print("=" * 60)
        print(f"Erro: {e}")
        return False


def criar_readme_dist():
    """Cria README para a distribuição"""
    readme_content = """# Baixador de Cadernos PJe

## Como Usar

1. Execute `BaixadorCadernosPJe.exe`
2. O navegador abrirá automaticamente
3. Configure a pasta de salvamento
4. Baixe os cadernos desejados
5. Use a busca para encontrar termos nos documentos

## Importante

- Mantenha a janela preta (console) aberta enquanto usar o programa
- Os arquivos serão salvos na pasta que você configurar
- A busca funciona apenas nos documentos já baixados

## Suporte

Para reportar problemas, entre em contato ou abra uma issue no repositório.

## Versão

Baixador de Cadernos PJe v1.0
"""

    dist_dir = 'dist'
    if os.path.exists(dist_dir):
        readme_path = os.path.join(dist_dir, 'LEIA-ME.txt')
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print(f"✓ Criado: {readme_path}")


def main():
    print("=" * 60)
    print("  BUILD - Baixador de Cadernos PJe (.exe)")
    print("=" * 60)

    # Verifica sistema operacional
    if sys.platform != 'win32':
        print("\n⚠️  AVISO: Este script gera .exe para Windows")
        print("   Você está em:", sys.platform)
        resposta = input("   Continuar mesmo assim? (s/n): ")
        if resposta.lower() != 's':
            print("Build cancelado.")
            return

    # Passo 1: Verificar PyInstaller
    if not verificar_pyinstaller():
        print("\n❌ Build cancelado - PyInstaller não disponível")
        return

    # Passo 2: Verificar dependências
    if not verificar_dependencias():
        print("\n❌ Build cancelado - Dependências faltando")
        return

    # Passo 3: Limpar builds antigos
    limpar_builds_antigos()

    # Passo 4: Criar executável
    if criar_executavel():
        # Passo 5: Criar README
        criar_readme_dist()

        print("\n" + "=" * 60)
        print("📦 EXECUTÁVEL CRIADO COM SUCESSO!")
        print("=" * 60)
        print("\nLocalização:")
        print(f"  📁 {os.path.abspath('dist/BaixadorCadernosPJe.exe')}")
        print("\nTamanho:")
        exe_path = 'dist/BaixadorCadernosPJe.exe'
        if os.path.exists(exe_path):
            tamanho_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"  📊 {tamanho_mb:.1f} MB")
        print("\nDistribuição:")
        print("  📦 Você pode distribuir o arquivo .exe")
        print("  💡 O usuário só precisa dar duplo clique!")
        print("  ⚠️  Antivírus podem dar falso positivo - é normal")
        print("\n" + "=" * 60)
    else:
        print("\n❌ Falha ao criar executável")
        print("Verifique os erros acima")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nBuild cancelado pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
