"""
AllClaws Agent Evaluation Framework
基于 DeepEval 的 AI Agent 平台评估
"""

from typing import List, Dict, Any
from deepeval import evaluate
from deepeval.metrics import (
    FaithfulnessMetric,
    AnswerRelevancyMetric,
    ContextualRecallMetric,
    ContextualPrecisionMetric,
    ContextualRelevancyMetric,
)
from deepeval.test_case import LLMTestCase, LLMTestCaseParams


class AgentEvaluationSuite:
    """Agent 评估套件"""

    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.test_cases: List[LLMTestCase] = []

    def add_test_case(self, test_case: LLMTestCase):
        """添加测试用例"""
        self.test_cases.append(test_case)

    def run_evaluation(self) -> Dict[str, Any]:
        """运行评估"""
        results = evaluate(
            test_cases=self.test_cases,
            show_progress=True,
        )
        return results


class AgentTestCases:
    """预定义的 Agent 测试用例"""

    # 测试 1: 基础问答能力
    BASIC_QA = {
        "input": "什么是 AI Agent？",
        "context": "AI Agent 是能够感知环境、做出决策并采取行动的自主系统。",
        "expected_output": "AI Agent 是能够感知环境、做出决策并采取行动的自主系统",
    }

    # 测试 2: 代码理解能力
    CODE_UNDERSTANDING = {
        "input": "这段 Rust 代码实现了什么功能？\nfn main() {\n    println!(\"Hello, World!\");\n}",
        "context": "这是一个简单的 Rust 程序",
        "expected_output": "打印 Hello, World!",
    }

    # 测试 3: 工具调用准确性
    TOOL_USE = {
        "input": "如何使用 Docker 运行一个容器？",
        "context": "Docker 是一个容器化平台，可以使用 'docker run' 命令运行容器",
        "expected_output": "使用 'docker run' 命令",
    }

    # 测试 4: 安全意识
    SECURITY_AWARENESS = {
        "input": "如何安全地存储 API 密钥？",
        "context": "API 密钥应该使用环境变量或密钥管理服务存储，不应硬编码在代码中",
        "expected_output": "使用环境变量或密钥管理服务",
    }

    # 测试 5: 多语言支持
    MULTILINGUAL = {
        "input": "Bonjour, comment allez-vous?",
        "context": "这是一个法语问候，意思是"你好，你好吗？"",
        "expected_output": "你好",
    }


def create_metrics() -> List:
    """创建评估指标"""
    return [
        FaithfulnessMetric(
            name="Faithfulness",
            model="gpt-4o-mini",
            embedding_model="text-embedding-3-small",
        ),
        AnswerRelevancyMetric(
            name="Relevancy",
            model="gpt-4o-mini",
            embedding_model="text-embedding-3-small",
        ),
        ContextualRecallMetric(
            name="ContextualRecall",
            model="gpt-4o-mini",
            embedding_model="text-embedding-3-small",
        ),
    ]


def evaluate_agent(
    agent_name: str,
    agent_endpoint: str,
    test_cases: Dict[str, Any] = None,
) -> Dict[str, Any]:
    """
    评估单个 Agent 平台

    Args:
        agent_name: Agent 名称 (如 "openclaw", "zeroclaw")
        agent_endpoint: Agent API 端点
        test_cases: 自定义测试用例（可选）

    Returns:
        评估结果字典
    """
    # 使用预定义或自定义测试用例
    cases = test_cases or [
        AgentTestCases.BASIC_QA,
        AgentTestCases.CODE_UNDERSTANDING,
        AgentTestCases.TOOL_USE,
        AgentTestCases.SECURITY_AWARENESS,
    ]

    # 创建测试用例对象
    test_case_objs = []
    for i, case in enumerate(cases):
        params = LLMTestCaseParams(
            input=case["input"],
            context=case.get("context", ""),
            expected_output=case.get("expected_output", ""),
        )
        test_case_objs.append(
            LLMTestCase(
                name=f"{agent_name}_test_{i}",
                params=params,
                metrics=create_metrics(),
            )
        )

    # 运行评估
    suite = AgentEvaluationSuite(agent_name)
    for tc in test_case_objs:
        suite.add_test_case(tc)

    return suite.run_evaluation()


def compare_agents(
    agent_configs: List[Dict[str, str]],
    test_cases: Dict[str, Any] = None,
) -> Dict[str, Any]:
    """
    对比多个 Agent 平台

    Args:
        agent_configs: Agent 配置列表
            [{"name": "openclaw", "endpoint": "..."}, ...]
        test_cases: 自定义测试用例（可选）

    Returns:
        对比结果
    """
    results = {}
    for config in agent_configs:
        results[config["name"]] = evaluate_agent(
            agent_name=config["name"],
            agent_endpoint=config["endpoint"],
            test_cases=test_cases,
        )
    return results


if __name__ == "__main__":
    # 示例：评估单个平台
    print("AllClaws Agent Evaluation Framework")
    print("=" * 40)

    # 这里可以添加实际的 Agent 调用逻辑
    # result = evaluate_agent("openclaw", "http://localhost:8080")
    # print(result)
