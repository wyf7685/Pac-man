# Pac-man


## 简介
  使用 `pygame` 模块编写的吃豆人小游戏
  

## 运行方法
  1. 执行 `poetry install` 命令，使用 `poetry` 包管理器创建虚拟环境。
   
  2. 执行 `poetry run Game.py` 命令，开始游戏。

  3. 使用方向键 (`↑↓←→`) 控制角色移动。

## 程序说明

  - `Game.py`
    
    主程序文件，包含游戏主循环及主要逻辑。

  - `Const.py`

    定义常量，包含资源路径和颜色RGB元组。

  - `Levels.py`

    定义关卡数据，通过继承`Level`基类并实现对应方法来创建关卡。
    
    `LEVELS` 数组保存各关卡类对象，代码中目前仅创建第一关，可继续继承`Level`类实现多关卡。

  - `Sprites.py`

    定义游戏中各实体，继承自 `pygame.sprites.Sprite` 类，包含 `Wall`, `Food`, `Ghost`, `Hero`，实现游戏内各实体的交互。

  - `Maze.py`

    包含一个`BFS`算法实现的迷宫寻路函数，用于在游戏中实现`Ghost`的寻路能力。


## 贡献者

  - [`Jackpot-Z`](https://github.com/Jackpot-Z)
  - [`wyf7685`](https://github.com/wyf7685)

