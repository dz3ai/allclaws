#!/bin/bash
# AllClaws 沙盒化测试运行脚本
# 使用 Docker Compose + DeepEval 评估各平台

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRAMEWORK_DIR="$(dirname "$SCRIPT_DIR")"
ALLCLAWS_DIR="$(dirname "$FRAMEWORK_DIR")"

echo "=========================================="
echo " AllClaws Sandbox Testing Framework"
echo " $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="
echo ""

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 步骤 1: 启动沙盒环境
echo -e "${YELLOW}步骤 1/4: 启动 Docker 沙盒环境...${NC}"
cd "$FRAMEWORK_DIR"
docker-compose up -d 2>&1 | tail -5
echo -e "${GREEN}✓ 沙盒环境已启动${NC}"
echo ""

# 步骤 2: 初始化 DeepEval
echo -e "${YELLOW}步骤 2/4: 初始化评估框架...${NC}"
if ! docker exec deepeval-runner pip list | grep -q deepeval; then
    docker exec deepeval-runner pip install deepeval pytest pytest-asyncio jq > /dev/null 2>&1
fi
echo -e "${GREEN}✓ DeepEval 已初始化${NC}"
echo ""

# 步骤 3: 运行静态分析测试
echo -e "${YELLOW}步骤 3/4: 运行静态分析测试...${NC}"
bash "$SCRIPT_DIR/run_tests.sh" 2>&1 | grep -E "PASS|FAIL|Total" | tail -5
echo -e "${GREEN}✓ 静态分析完成${NC}"
echo ""

# 步骤 4: 运行基准测试
echo -e "${YELLOW}步骤 4/4: 运行基准测试...${NC}"
bash "$SCRIPT_DIR/run_benchmarks.sh" 2>&1 | grep -E "pass|fail|Total" | tail -3
echo -e "${GREEN}✓ 基准测试完成${NC}"
echo ""

# 清理（可选）
# echo -e "${YELLOW}清理沙盒环境...${NC}"
# docker-compose down

echo "=========================================="
echo -e "${GREEN}测试完成！${NC}"
echo "=========================================="
echo ""
echo "查看结果:"
echo "  - 测试报告: cat results/latest/results.md"
echo "  - 基准报告: cat benchmark_results/latest/benchmark_results.md"
echo "  - 结果服务器: http://localhost:8080 (如果已启动)"
echo ""
