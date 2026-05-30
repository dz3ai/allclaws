---
layout: post
title: "robot-toolkit: 开源 6-DOF 机械臂工具箱发布 v0.3.0"
date: 2026-05-29 22:00:00 +0800
author: Danny Zeng
categories: [Open Source]
tags: [robotics, inverse-kinematics, dynamics, python, open-source, PyPI, C++]
---

## 一句话

robot-ik 0.3.0 现已发布至 PyPI，一行 `pip install robot-ik` 即可获得完整的 6-DOF 串联机械臂工程工具箱。

```
pip install robot-ik
```

---

## 这是什么

robot-toolkit 是一个面向 6-DOF 串联机械臂的 Python 工具箱，涵盖从运动学到动力学的完整计算管线。设计理念类似 numpy/scipy 在机器人领域的定位——独立、可组合的模块。

**核心能力：**

- 运动学：DH 参数正运动学 + 阻尼最小二乘逆运动学（Levenberg-Marquardt）
- 动力学：RNEA 逆动力学 + CRBA 正动力学
- 轨迹规划：线性/三次/五次插值、梯形速度、S 曲线、笛卡尔直线、waypoint
- 碰撞检测：球体/胶囊/包围盒、自碰撞、环境障碍物
- 路径规划：RRT* 碰撞避免路径规划
- URDF 解析：从 URDF 提取质量/惯量并生成动力学模型
- 3D 可视化：matplotlib + meshcat（Web 端，支持 Jupyter）
- 硬件抽象层：统一接口 + 注册表模式，支持模拟/ROS2/自定义后端

## C++ 加速

纯 Python 的 IK 求解约 12.6 ms，C++ 扩展降至 0.09 ms（**137 倍加速**）。动力学计算同样有 C++ 实现，358 倍加速。

C++ 扩展是可选的——未编译时自动降级到纯 Python，无需任何额外配置。

## 快速上手

```python
from robot_ik import six_dof_articulated
import numpy as np

robot = six_dof_articulated()

target = np.array([
    [0, -1,  0, 0.5],
    [0,  0, -1, 0.2],
    [1,  0,  0, 0.4],
    [0,  0,  0, 1.0],
])

success, angles, iters, errors = robot.ik_solve(target)
print(f"Solved in {iters} iterations, angles: {angles}")
```

## 可选安装

```bash
pip install robot-ik              # 核心（仅 numpy 依赖）
pip install robot-ik[viz]         # + matplotlib 可视化
pip install robot-ik[meshcat]     # + meshcat Web 3D 可视化
pip install robot-ik[all]         # 全部可选依赖
```

## 项目结构

```
src/robot_ik/         # 8 个子模块
├── ik/               # IK 求解器 + C++ 扩展
├── dynamics/         # 刚体动力学
├── trajectory/       # 轨迹规划
├── collision/        # 碰撞检测
├── path_planning/    # RRT* 路径规划
├── urdf/             # URDF 解析
├── visualization/    # matplotlib + meshcat
└── hardware/         # 硬件抽象层
```

67 个测试，ruff + black 检查全部通过。CI 覆盖 Linux / macOS（自托管 M1） / Windows，Python 3.10-3.12。

## 人机协作开发

这个项目是一次人机协作开发的实践。AI Agent 承担了大部分编码工作——从初始 IK 求解器到动力学模块、碰撞检测、路径规划，以及 C++ pybind11 扩展。人类负责架构决策、代码审查和方向把控。

关键协作模式：

- **Agent 实现 → 人 Review**：Agent 完成模块后，人类通过 code review 确认质量
- **Agent 规划 → 人审批 → Agent 执行**：复杂任务先写计划，人类确认后分步执行
- **人类提出需求 → Agent 自主实现**：如"把测试按模块分组"这类明确任务直接交给 Agent

完整的 15 个阶段开发过程，包括踩过的坑（macOS CI 超时 24 小时、setuptools 环境变量问题），都记录在项目的 ROADMAP.md 中。

## 链接

- **PyPI**: https://pypi.org/project/robot-ik/
- **GitHub**: https://github.com/DZ-drawing/robot-toolkit
- **MIT 开源**
