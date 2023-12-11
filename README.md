# Pac-man


## 简介 | Introduction
  使用 `pygame` 模块编写的吃豆人小游戏
  

## 运行方法 | Usage
  1. 执行 `poetry install` 命令，使用 `poetry` 包管理器创建虚拟环境。
   
  2. 执行 `poetry run python main.py` 命令，开始游戏。

  3. 使用方向键 (`↑↓←→`) 控制角色移动。

## 程序说明 | Description

  - `main.py`
    
    主程序文件，包含游戏主循环及主要逻辑。

  - `src/const.py`

    定义常量，包含资源路径和颜色RGB元组。

  - `src/level.py`

    定义关卡信息，`Level`类通过读取`assets/levels/`目录下的json文件创建关卡。
    
    `LEVELS` 数组保存各关卡对象。
    
    `assets/levels/`中目前仅创建第一关(`1.json`)，可以通过编写json文件创建新关卡，json文件参数含义见`src/level.py`注释。

  - `src/sprites/*.py`

    定义游戏中各实体，继承自 `pygame.sprites.Sprite` 类，包含 `Wall`, `Food`, `Ghost`, `Hero`，实现游戏内各实体的交互。

  - `src/maze.py`

    包含一个`BFS`算法实现的迷宫寻路函数，用于在游戏中实现`Ghost`的寻路能力。


## 贡献者 | Contributors

  ![Contributors](https://contrib.rocks/image?repo=wyf7685/Pac-man)

