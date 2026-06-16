#!/usr/bin/env sh
# install.sh — установка пакета gost732-2017 в локальный namespace Typst.
#
# Автономный установщик: ставит ТОЛЬКО gost732-2017 (в отличие от комбайна
# typst-bmstu, который тянет сразу два пакета и кладёт их в namespace `local`).
# Работает в двух режимах, выбор автоматический:
#   * локальный — если рядом лежит gost732-2017/typst.toml (запуск из клона),
#                 ставит из него, версию берёт из typst.toml;
#   * git clone — иначе клонирует апстрим и берёт нужный тег (для `curl | sh`).
#
# Поддержка: Linux, macOS. Для Windows — install.ps1.
#
# Использование:
#   ./install.sh [версия] [флаги]
#   curl -fsSL <raw>/install.sh | sh -s -- [версия] [флаги]
#
# Флаги:
#   --with-typst       доустановить бинарь typst без вопросов
#   --no-typst         не трогать бинарь typst (для CI / `curl | sh`)
#   --namespace NAME   namespace пакета (по умолчанию docs)
#   --link             симлинк вместо копирования (только локальный режим)
#   -h, --help         показать помощь
#
# Переменные окружения:
#   TYPST_NAMESPACE      то же, что --namespace
#   TYPST_PACKAGE_PATH   переопределить каталог packages целиком
#
# pluttan

set -eu

PKG_NAME="gost732-2017"
REPO_URL="https://github.com/bmstudents/typst-g7.32-2017.git"
REQUIRED_TYPST="0.14.2"   # из gost732-2017/typst.toml (compiler)

# ── оформление вывода (палитра Catppuccin Mocha, 256 цветов) ───────────────
if [ -t 1 ]; then
    e="$(printf '\033')"
    C_OFF="${e}[0m";          C_B="${e}[1m"
    C_MAUVE="${e}[38;5;141m"; C_GRN="${e}[38;5;114m"
    C_YEL="${e}[38;5;222m";   C_RED="${e}[38;5;211m"
    C_TEAL="${e}[38;5;116m";  C_DIM="${e}[38;5;245m"
else
    C_OFF=""; C_B=""; C_MAUVE=""; C_GRN=""; C_YEL=""; C_RED=""; C_TEAL=""; C_DIM=""
fi
info() { printf '  %s❯%s %s\n' "$C_MAUVE" "$C_OFF" "$1"; }
ok()   { printf '  %s✓%s %s\n' "$C_GRN"   "$C_OFF" "$1"; }
warn() { printf '  %s!%s %s\n' "$C_YEL"   "$C_OFF" "$1" >&2; }
err()  { printf '  %s✗%s %s\n' "$C_RED"   "$C_OFF" "$1" >&2; }

banner() {
    printf '\n'
    printf '  %s┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓%s\n' "$C_MAUVE" "$C_OFF"
    printf '  %s┃%s  %s%sgost732-2017%s  %s· установка пакета%s\n' \
        "$C_MAUVE" "$C_OFF" "$C_B" "$C_MAUVE" "$C_OFF" "$C_DIM" "$C_OFF"
    printf '  %s┃%s  %sстили оформления по ГОСТ 7.32-2017 для Typst%s\n' \
        "$C_MAUVE" "$C_OFF" "$C_DIM" "$C_OFF"
    printf '  %s┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛%s\n' "$C_MAUVE" "$C_OFF"
    printf '\n'
}

usage() {
    sed -n '2,27p' "$0" | sed 's/^# \{0,1\}//'
}

# ── разбор аргументов ─────────────────────────────────────────────────────
VERSION=""
WITH_TYPST="ask"                       # ask | yes | no
NAMESPACE="${TYPST_NAMESPACE:-docs}"
LINK=0
while [ $# -gt 0 ]; do
    case "$1" in
        --with-typst)   WITH_TYPST="yes" ;;
        --no-typst)     WITH_TYPST="no" ;;
        --namespace)    shift; NAMESPACE="${1:?--namespace требует значение}" ;;
        --namespace=*)  NAMESPACE="${1#*=}" ;;
        --link)         LINK=1 ;;
        -h|--help)      usage; exit 0 ;;
        -*)             err "неизвестный флаг: $1"; usage; exit 1 ;;
        *)              VERSION="$1" ;;
    esac
    shift
done

banner

# ── каталог пакетов Typst (как его ищет компилятор через крейт dirs) ───────
if [ -n "${TYPST_PACKAGE_PATH:-}" ]; then
    packages="$TYPST_PACKAGE_PATH"
elif [ "$(uname -s)" = "Darwin" ]; then
    packages="$HOME/Library/Application Support/typst/packages"
else
    packages="${XDG_DATA_HOME:-$HOME/.local/share}/typst/packages"
fi

# ── версия из typst.toml ──────────────────────────────────────────────────
read_toml_version() {
    sed -n 's/^[[:space:]]*version[[:space:]]*=[[:space:]]*"\([^"]*\)".*/\1/p' "$1" \
        | head -n1
}

# ── выбор источника: локальный клон или git clone апстрима ─────────────────
script_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
src=""
mode=""
ver=""

if [ -f "$script_dir/$PKG_NAME/typst.toml" ]; then
    mode="local"
    src="$script_dir/$PKG_NAME"
elif [ -f "$script_dir/typst.toml" ] && grep -q "name = \"$PKG_NAME\"" "$script_dir/typst.toml"; then
    # скрипт лежит внутри самого каталога пакета
    mode="local"
    src="$script_dir"
else
    mode="clone"
fi

if [ "$mode" = "local" ]; then
    ver="${VERSION:-$(read_toml_version "$src/typst.toml")}"
    [ -n "$ver" ] || { err "не удалось определить версию из $src/typst.toml"; exit 1; }
    info "Локальный режим: $src (версия $ver)"
else
    command -v git >/dev/null 2>&1 || { err "нужен git для режима clone"; exit 1; }
    tmp="$(mktemp -d)"
    trap 'rm -rf "$tmp"' EXIT INT TERM
    if [ -n "$VERSION" ] && [ "$VERSION" != "latest" ]; then
        info "Клонирую $PKG_NAME тег $VERSION"
        git clone --depth 1 --branch "$VERSION" "$REPO_URL" "$tmp/repo" >/dev/null 2>&1 \
            || { err "не удалось склонировать тег $VERSION"; exit 1; }
        ver="$VERSION"
    else
        info "Клонирую $PKG_NAME (последний тег)"
        git clone "$REPO_URL" "$tmp/repo" >/dev/null 2>&1 \
            || { err "не удалось склонировать $REPO_URL"; exit 1; }
        ver="$(git -C "$tmp/repo" describe --tags "$(git -C "$tmp/repo" rev-list --tags --max-count=1)")"
        git -C "$tmp/repo" checkout -q "$ver"
    fi
    src="$tmp/repo/$PKG_NAME"
    [ -f "$src/typst.toml" ] || { err "в склонированном репозитории нет $PKG_NAME/typst.toml"; exit 1; }
fi

# ── установка в namespace ──────────────────────────────────────────────────
target="$packages/$NAMESPACE/$PKG_NAME/$ver"
info "Устанавливаю в $target"

if [ -e "$target" ] || [ -L "$target" ]; then
    warn "уже существует — переустанавливаю"
    rm -rf "$target"
fi
mkdir -p "$(dirname "$target")"

if [ "$LINK" = "1" ]; then
    if [ "$mode" != "local" ]; then
        err "--link работает только в локальном режиме (clone живёт во временной папке)"
        exit 1
    fi
    ln -s "$src" "$target"
    ok "симлинк $target → $src"
else
    mkdir -p "$target"
    cp -R "$src/." "$target/"
    ok "пакет скопирован"
fi

# ── бинарь typst ───────────────────────────────────────────────────────────
install_typst() {
    command -v curl >/dev/null 2>&1 || { err "нужен curl для установки typst"; return 1; }
    case "$(uname -sm)" in
        "Darwin x86_64") tgt="x86_64-apple-darwin" ;;
        "Darwin arm64")  tgt="aarch64-apple-darwin" ;;
        "Linux aarch64") tgt="aarch64-unknown-linux-musl" ;;
        *)               tgt="x86_64-unknown-linux-musl" ;;
    esac
    folder="typst-$tgt"
    url="https://github.com/typst/typst/releases/download/v$REQUIRED_TYPST/$folder.tar.xz"
    dest="${TYPST_INSTALL:-$HOME/.typst}"
    mkdir -p "$dest"
    info "Скачиваю typst $REQUIRED_TYPST ($tgt)"
    curl -fsSL "$url" -o "$dest/$folder.tar.xz" \
        || { err "не удалось скачать typst с $url"; return 1; }
    tar -xJf "$dest/$folder.tar.xz" -C "$dest"
    rm -f "$dest/$folder.tar.xz"
    mkdir -p "$dest/bin"
    mv -f "$dest/$folder/typst" "$dest/bin/typst"
    chmod +x "$dest/bin/typst"
    rm -rf "$dest/$folder"
    ok "typst установлен → $dest/bin/typst"
    if ! command -v typst >/dev/null 2>&1; then
        warn "добавь в PATH:  export PATH=\"$dest/bin:\$PATH\""
    fi
}

ensure_typst() {
    have=""
    if command -v typst >/dev/null 2>&1; then
        have="$(typst --version 2>/dev/null | awk '{print $2}')"
    fi
    if [ "$have" = "$REQUIRED_TYPST" ]; then
        ok "typst $have — ок"
        return 0
    fi
    case "$WITH_TYPST" in
        yes) install_typst ;;
        no)  warn "нужен typst $REQUIRED_TYPST (найдено: ${have:-нет}). Пропускаю (--no-typst)." ;;
        ask)
            # читаем с управляющего терминала, а не из stdin — иначе при
            # `curl … | sh` stdin занят скриптом и вопрос не задаётся.
            if [ -e /dev/tty ]; then
                printf '  %s?%s Нужен typst %s (найдено: %s). Установить? [y/N] ' \
                    "$C_YEL" "$C_OFF" "$REQUIRED_TYPST" "${have:-нет}" > /dev/tty
                IFS= read -r ans < /dev/tty || ans=""
                case "$ans" in
                    [Yy]*) install_typst ;;
                    *)     warn "пропускаю установку typst (поставь сам или запусти с --with-typst)" ;;
                esac
            else
                warn "нужен typst $REQUIRED_TYPST (найдено: ${have:-нет}). Запусти с --with-typst или поставь вручную."
            fi
            ;;
    esac
}

ensure_typst

# ── итог ────────────────────────────────────────────────────────────────────
printf '\n'
printf '  %s%s✓ Готово%s  %s· пакет в namespace @%s%s\n' \
    "$C_B" "$C_GRN" "$C_OFF" "$C_DIM" "$NAMESPACE" "$C_OFF"
printf '\n'
printf '    %sподключение в .typ:%s\n' "$C_DIM" "$C_OFF"
printf '    %s%s#import "@%s/%s:%s": *%s\n' \
    "$C_B" "$C_TEAL" "$NAMESPACE" "$PKG_NAME" "$ver" "$C_OFF"
printf '\n'
