#!/usr/bin/env pwsh
# install.ps1 — установка пакета gost732-2017 в локальный namespace Typst (Windows).
#
# Автономный установщик: ставит ТОЛЬКО gost732-2017 (в отличие от комбайна
# typst-bmstu). Работает в двух режимах, выбор автоматический:
#   * локальный — если рядом лежит gost732-2017\typst.toml (запуск из клона),
#                 ставит из него, версию берёт из typst.toml;
#   * git clone — иначе клонирует апстрим и берёт нужный тег.
#
# Зеркало install.sh. Для Linux/macOS — install.sh.
#
# Использование:
#   .\install.ps1 [-Version <тег>] [-WithTypst] [-NoTypst] [-Namespace docs] [-Link]
#   irm <raw>/install.ps1 | iex          # последняя версия из апстрима
#
# pluttan

[CmdletBinding()]
param(
    [string]$Version = "",
    [switch]$WithTypst,
    [switch]$NoTypst,
    [string]$Namespace = $(if ($env:TYPST_NAMESPACE) { $env:TYPST_NAMESPACE } else { "docs" }),
    [switch]$Link,
    [switch]$Help
)

$ErrorActionPreference = "Stop"

$PkgName       = "gost732-2017"
$RepoUrl       = "https://github.com/bmstudents/typst-g7.32-2017.git"
$RequiredTypst = "0.14.2"   # из gost732-2017/typst.toml (compiler)

# ── оформление вывода (палитра Catppuccin Mocha, 256 цветов) ───────────────
$E = [char]27
if ($Host.UI.SupportsVirtualTerminal) {
    $COff = "$E[0m";          $CB = "$E[1m"
    $CMauve = "$E[38;5;141m"; $CGrn = "$E[38;5;114m"
    $CYel = "$E[38;5;222m";   $CRed = "$E[38;5;211m"
    $CTeal = "$E[38;5;116m";  $CDim = "$E[38;5;245m"
} else {
    $COff = ""; $CB = ""; $CMauve = ""; $CGrn = ""
    $CYel = ""; $CRed = ""; $CTeal = ""; $CDim = ""
}
function Info($m) { Write-Host "  $CMauve❯$COff $m" }
function Ok($m)   { Write-Host "  $CGrn✓$COff $m" }
function Warn($m) { Write-Host "  $CYel!$COff $m" }
function Err($m)  { Write-Host "  $CRed✗$COff $m" }
function Banner {
    Write-Host ""
    Write-Host "  $CMauve┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓$COff"
    Write-Host "  $CMauve┃$COff  $CB${CMauve}gost732-2017$COff  $CDim· установка пакета$COff"
    Write-Host "  $CMauve┃$COff  ${CDim}стили оформления по ГОСТ 7.32-2017 для Typst$COff"
    Write-Host "  $CMauve┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛$COff"
    Write-Host ""
}

if ($Help) {
    Get-Content $PSCommandPath | Select-Object -Skip 1 -First 25 |
        ForEach-Object { $_ -replace '^#\s?', '' }
    exit 0
}

Banner

# ── каталог пакетов Typst ──────────────────────────────────────────────────
if ($env:TYPST_PACKAGE_PATH) {
    $packages = $env:TYPST_PACKAGE_PATH
} else {
    $packages = Join-Path $env:APPDATA "typst\packages"
}

function Read-TomlVersion($tomlPath) {
    foreach ($line in Get-Content $tomlPath) {
        if ($line -match '^\s*version\s*=\s*"([^"]+)"') { return $Matches[1] }
    }
    return $null
}

# ── выбор источника ────────────────────────────────────────────────────────
$scriptDir = Split-Path -Parent $PSCommandPath
$src  = $null
$mode = $null
$ver  = $null

$localToml = Join-Path $scriptDir "$PkgName\typst.toml"
$selfToml  = Join-Path $scriptDir "typst.toml"
if (Test-Path $localToml) {
    $mode = "local"
    $src  = Join-Path $scriptDir $PkgName
} elseif ((Test-Path $selfToml) -and ((Get-Content $selfToml) -match "name = `"$PkgName`"")) {
    $mode = "local"
    $src  = $scriptDir
} else {
    $mode = "clone"
}

if ($mode -eq "local") {
    if ($Version) { $ver = $Version } else { $ver = Read-TomlVersion (Join-Path $src "typst.toml") }
    if (-not $ver) { Err "не удалось определить версию из typst.toml"; exit 1 }
    Info "Локальный режим: $src (версия $ver)"
} else {
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) { Err "нужен git для режима clone"; exit 1 }
    $tmp = Join-Path ([System.IO.Path]::GetTempPath()) ("gost732-" + [System.IO.Path]::GetRandomFileName())
    New-Item -ItemType Directory -Path $tmp -Force | Out-Null
    if ($Version -and $Version -ne "latest") {
        Info "Клонирую $PkgName тег $Version"
        git clone --depth 1 --branch $Version $RepoUrl "$tmp\repo" 2>$null
        if ($LASTEXITCODE -ne 0) { Err "не удалось склонировать тег $Version"; exit 1 }
        $ver = $Version
    } else {
        Info "Клонирую $PkgName (последний тег)"
        git clone $RepoUrl "$tmp\repo" 2>$null
        if ($LASTEXITCODE -ne 0) { Err "не удалось склонировать $RepoUrl"; exit 1 }
        $latestTag = git -C "$tmp\repo" rev-list --tags --max-count=1
        $ver = git -C "$tmp\repo" describe --tags $latestTag
        git -C "$tmp\repo" checkout -q $ver
    }
    $src = Join-Path $tmp "repo\$PkgName"
    if (-not (Test-Path (Join-Path $src "typst.toml"))) { Err "в репозитории нет $PkgName\typst.toml"; exit 1 }
}

# ── установка в namespace ──────────────────────────────────────────────────
$target = Join-Path $packages "$Namespace\$PkgName\$ver"
Info "Устанавливаю в $target"

if (Test-Path $target) {
    Warn "уже существует — переустанавливаю"
    Remove-Item -Recurse -Force $target
}
New-Item -ItemType Directory -Path (Split-Path -Parent $target) -Force | Out-Null

if ($Link) {
    if ($mode -ne "local") { Err "-Link работает только в локальном режиме"; exit 1 }
    # junction не требует прав администратора, в отличие от symlink
    New-Item -ItemType Junction -Path $target -Target $src | Out-Null
    Ok "junction $target -> $src"
} else {
    New-Item -ItemType Directory -Path $target -Force | Out-Null
    Copy-Item -Path (Join-Path $src "*") -Destination $target -Recurse -Force
    Ok "пакет скопирован"
}

# ── бинарь typst ───────────────────────────────────────────────────────────
function Install-Typst {
    $folder = "typst-x86_64-pc-windows-msvc"
    $url  = "https://github.com/typst/typst/releases/download/v$RequiredTypst/$folder.zip"
    $dest = if ($env:TYPST_INSTALL) { $env:TYPST_INSTALL } else { Join-Path $env:USERPROFILE ".typst" }
    New-Item -ItemType Directory -Path $dest -Force | Out-Null
    Info "Скачиваю typst $RequiredTypst (x86_64-pc-windows-msvc)"
    curl.exe -fsSL "$url" -o "$dest\$folder.zip"
    if ($LASTEXITCODE -ne 0) { Err "не удалось скачать typst"; return }
    tar.exe -xf "$dest\$folder.zip" -C "$dest"
    Remove-Item "$dest\$folder.zip"

    $user = [System.EnvironmentVariableTarget]::User
    $path = [System.Environment]::GetEnvironmentVariable("Path", $user)
    $binDir = "$dest\$folder"
    if (";$path;".ToLower() -notlike "*;$($binDir.ToLower());*") {
        [System.Environment]::SetEnvironmentVariable("Path", "$path;$binDir", $user)
        $env:Path += ";$binDir"
    }
    Ok "typst установлен -> $binDir\typst.exe (PATH обновлён для пользователя)"
}

function Get-TypstVersion {
    $cmd = Get-Command typst -ErrorAction SilentlyContinue
    if (-not $cmd) { return $null }
    $out = (& typst --version) 2>$null
    if ($out -match '(\d+\.\d+\.\d+)') { return $Matches[1] }
    return $null
}

$have = Get-TypstVersion
if ($have -eq $RequiredTypst) {
    Ok "typst $have - ок"
} elseif ($NoTypst) {
    Warn "нужен typst $RequiredTypst (найдено: $(if($have){$have}else{'нет'})). Пропускаю (-NoTypst)."
} elseif ($WithTypst) {
    Install-Typst
} else {
    $found = if ($have) { $have } else { "нет" }
    $ans = Read-Host "Нужен typst $RequiredTypst (найдено: $found). Установить? [y/N]"
    if ($ans -match '^[Yy]') { Install-Typst } else { Warn "пропускаю установку typst" }
}

# ── итог ────────────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "  $CB$CGrn✓ Готово$COff  $CDim· пакет в namespace @$Namespace$COff"
Write-Host ""
Write-Host "    ${CDim}подключение в .typ:$COff"
Write-Host "    $CB$CTeal#import `"@$Namespace/$PkgName`:$ver`": *$COff"
Write-Host ""
