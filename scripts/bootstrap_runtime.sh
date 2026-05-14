#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUNTIME_DIR="${RUNTIME_DIR:-$ROOT_DIR/.runtime}"
CONDA_DIR="$RUNTIME_DIR/miniconda"
PY_ENV_DIR="$RUNTIME_DIR/py311"
FRONT_DIR="$ROOT_DIR/frontend"
NODE_VERSION="${NODE_VERSION:-}"
NVM_DIR="${NVM_DIR:-$HOME/.nvm}"

if [ -z "$NODE_VERSION" ]; then
  if [ -f "$FRONT_DIR/.nvmrc" ]; then
    NODE_VERSION="$(tr -d '[:space:]' < "$FRONT_DIR/.nvmrc")"
  else
    NODE_VERSION="v22.21.1"
  fi
fi

log() {
  printf '[bootstrap] %s\n' "$*"
}

download() {
  local url="$1"
  local output="$2"
  if command -v curl >/dev/null 2>&1; then
    curl -fsSL "$url" -o "$output"
  elif command -v wget >/dev/null 2>&1; then
    wget -q "$url" -O "$output"
  else
    log "未找到 curl/wget，无法下载安装包"
    exit 1
  fi
}

install_miniconda() {
  if [ -x "$CONDA_DIR/bin/conda" ]; then
    log "已存在 Miniconda: $CONDA_DIR"
    return 0
  fi

  local arch
  case "$(uname -m)" in
    x86_64) arch="x86_64" ;;
    aarch64|arm64) arch="aarch64" ;;
    *)
      log "不支持的系统架构: $(uname -m)"
      exit 1
      ;;
  esac

  mkdir -p "$RUNTIME_DIR"
  local installer="$RUNTIME_DIR/miniconda.sh"
  log "下载 Miniconda 安装器"
  download "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-${arch}.sh" "$installer"
  log "安装 Miniconda 到 $CONDA_DIR"
  bash "$installer" -b -p "$CONDA_DIR"
}

install_python() {
  if [ -x "$PY_ENV_DIR/bin/python" ]; then
    log "已存在 Python 环境: $PY_ENV_DIR"
    return 0
  fi

  log "接受 conda 默认 channel Terms of Service"
  "$CONDA_DIR/bin/conda" tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main || true
  "$CONDA_DIR/bin/conda" tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r || true

  log "创建 Python 3.11 环境"
  "$CONDA_DIR/bin/conda" create -y -p "$PY_ENV_DIR" python=3.11 pip
}

install_nvm_node() {
  if [ ! -s "$NVM_DIR/nvm.sh" ]; then
    log "安装 nvm 到 $NVM_DIR"
    download "https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh" "$RUNTIME_DIR/nvm-install.sh"
    PROFILE=/dev/null bash "$RUNTIME_DIR/nvm-install.sh"
  fi

  # shellcheck source=/dev/null
  . "$NVM_DIR/nvm.sh"
  log "安装/切换 Node $NODE_VERSION"
  nvm install "$NODE_VERSION"
  nvm use "$NODE_VERSION"
}

install_miniconda
install_python
install_nvm_node

log "运行项目安装脚本"
PYTHON_BIN="$PY_ENV_DIR/bin/python" "$ROOT_DIR/install.sh"
