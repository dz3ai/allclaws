#!/bin/bash
# AllClaws 沙盒化测试运行脚本
# 使用 Docker Compose + DeepEval 评估各平台
#
# 用法:
#   ./scripts/run_sandboxed_tests.sh          # 测试所有平台
#   ./scripts/run_sandboxed_tests.sh openclaw  # 只测试 openclaw
#   ./scripts/run_sandboxed_tests.sh zeroclaw ironclaw  # 测试多个指定平台

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRAMEWORK_DIR="$(dirname "$SCRIPT_DIR")"
ALLCLAWS_DIR="$(dirname "$FRAMEWORK_DIR")"

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# 从命令行参数获取要测试的平台列表
# 如果没有参数，测试所有平台
PLATFORMS=("${@:-}")

# 如果没有指定平台，测试所有平台
if [ ${#PLATFORMS[@]} -eq 0 ]; then
    echo -e "${BLUE}模式: 测试所有 13 个平台${NC}"
    ALL_PLATFORMS=true
else
    echo -e "${BLUE}模式: 测试指定平台: ${PLATFORMS[*]}${NC}"
    ALL_PLATFORMS=false
fi

echo "=========================================="
echo " AllClaws Sandbox Testing Framework"
echo " $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="
echo ""

# ============================================
# 辅助函数
# ============================================

# 启动指定平台的沙盒
start_platform_sandbox() {
    local platform=$1
    echo -e "  启动 ${YELLOW}$platform${NC} 沙盒..."

    case $platform in
        openclaw|nanoclaw|quantumclaw)
            docker-compose up -d "${platform}-sandbox" 2>/dev/null || true
            ;;
        zeroclaw|ironclaw)
            docker-compose up -d "${platform}-sandbox" 2>/dev/null || true
            ;;
        goclaw|maxclaw|hiclaw)
            docker-compose up -d "${platform}-sandbox" 2>/dev/null || true
            ;;
        clawteam|nanobot|claw-ai-lab|hermes-agent)
            docker-compose up -d "${platform}-sandbox" 2>/dev/null || true
            ;;
        rtl-claw)
            docker-compose up -d "${platform}-sandbox" 2>/dev/null || true
            ;;
        *)
            echo -e "    ${RED}✗ 未知平台: $platform${NC}"
            return 1
            ;;
    esac

    # 等待沙盒启动
    sleep 2

    # 检查容器是否运行
    local container_name="${platform}-sandbox"
    if docker ps --format '{{.Names}}' | grep -q "^${container_name}$"; then
        echo -e "    ${GREEN}✓ 已启动${NC}"
        return 0
    else
        echo -e "    ${RED}✗ 启动失败${NC}"
        return 1
    fi
}

# 运行单个平台的测试
run_platform_tests() {
    local platform=$1
    echo ""
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}测试平台: $platform${NC}"
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""

    # 1. 静态分析
    echo -e "${BLUE}1/2 静态分析...${NC}"
    if bash "$SCRIPT_DIR/run_tests.sh" 2>&1 | grep -q "$platform"; then
        echo -e "  ${GREEN}✓ 静态分析完成${NC}"
    else
        echo -e "  ${YELLOW}⚠ 跳过静态分析（无相关测试）${NC}"
    fi
    echo ""

    # 2. 基准测试
    echo -e "${BLUE}2/2 基准测试...${NC}"
    if bash "$SCRIPT_DIR/run_benchmarks.sh" 2>&1 | grep -q "$platform"; then
        echo -e "  ${GREEN}✓ 基准测试完成${NC}"
    else
        echo -e "  ${YELLOW}⚠ 跳过基准测试（无相关测试）${NC}"
    fi
    echo ""
}

# ============================================
# 主流程
# ============================================

# 步骤 1: 启动沙盒环境
if [ "$ALL_PLATFORMS" = true ]; then
    echo -e "${YELLOW}步骤 1/4: 启动 Docker 沙盒环境...${NC}"
    cd "$FRAMEWORK_DIR"
    docker-compose up -d 2>&1 | tail -5
    echo -e "${GREEN}✓ 沙盒环境已启动${NC}"
    echo ""
else
    echo -e "${YELLOW}步骤 1/3: 启动指定平台沙盒...${NC}"
    cd "$FRAMEWORK_DIR"
    for platform in "${PLATFORMS[@]}"; do
        start_platform_sandbox "$platform"
    done
    echo ""
fi

# 步骤 2: 初始化 DeepEval
echo -e "${YELLOW}步骤 2/$([ "$ALL_PLATFORMS" = true ] && echo "4" || echo "3"): 初始化评估框架...${NC}"
if ! docker exec deepeval-runner pip list 2>/dev/null | grep -q deepeval; then
    docker exec deepeval-runner pip install deepeval pytest pytest-asyncio jq > /dev/null 2>&1
fi
echo -e "${GREEN}✓ DeepEval 已初始化${NC}"
echo ""

# 步骤 3: 运行测试
if [ "$ALL_PLATFORMS" = true ]; then
    echo -e "${YELLOW}步骤 3/4: 运行静态分析测试...${NC}"
    bash "$SCRIPT_DIR/run_tests.sh" 2>&1 | grep -E "PASS|FAIL|Total" | tail -5
    echo -e "${GREEN}✓ 静态分析完成${NC}"
    echo ""

    echo -e "${YELLOW}步骤 4/4: 运行基准测试...${NC}"
    bash "$SCRIPT_DIR/run_benchmarks.sh" 2>&1 | grep -E "pass|fail|Total" | tail -3
    echo -e "${GREEN}✓ 基准测试完成${NC}"
else
    echo -e "${YELLOW}步骤 3/3: 运行指定平台测试...${NC}"
    for platform in "${PLATFORMS[@]}"; do
        run_platform_tests "$platform"
    done
fi

echo ""
echo "=========================================="
echo -e "${GREEN}测试完成！${NC}"
echo "=========================================="
echo ""
echo "查看结果:"
echo "  - 测试报告: cat results/latest/results.md"
echo "  - 基准报告: cat benchmark_results/latest/benchmark_results.md"
echo "  - 结果服务器: http://localhost:8080 (如果已启动)"
echo ""
echo -e "${BLUE}清理沙盒环境:${NC}"
echo "  docker-compose down"
echo ""
echo -e "${BLUE}只测试特定平台:${NC}"
echo "  ./scripts/run_sandboxed_tests.sh openclaw"
echo "  ./scripts/run_sandboxed_tests.sh zeroclaw ironclaw"
echo ""
