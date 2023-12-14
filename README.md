# Pac-man

## 简介 / Introduction

使用 `pygame` 模块编写的吃豆人小游戏

## 运行方法 / Usage

1. 执行 `poetry install` 命令，使用 `poetry` 包管理器创建虚拟环境。

2. 执行 `poetry run python main.py` 命令，开始游戏。

3. 使用方向键 (`↑↓←→`) 控制角色移动。

## 程序说明 / Description

- `main.py`

  主程序文件，包含游戏主循环及主要逻辑。

- `src/const.py`

  定义常量，包含资源路径和颜色 RGB 元组。

- `src/level.py`

  定义关卡信息，`Level`类通过读取`assets/levels/`目录下的 json 文件创建关卡。

  `LEVELS` 数组保存各关卡对象。

  `assets/levels/`中目前仅创建第一关(`1.json`)，可以通过编写 json 文件创建新关卡，json 文件参数含义见`src/level.py`注释。

- `src/sprites/*.py`

  定义游戏中各实体，继承自 `pygame.sprites.Sprite` 类，包含 `Wall`, `Food`, `Ghost`, `Hero`，实现游戏内各实体的交互。

- `src/maze.py`

  包含一个`BFS`算法实现的迷宫寻路函数，用于在游戏中实现`Ghost`的寻路能力。

- `test.py`

  调试模式，运行时读取`assets/levels/dev.json`中的关卡数据，生成静态地图，并提供关卡编辑功能 (详见[调试模式](#调试模式--debug-mode))。

## 调试模式 / Debug Mode

调试模式可以通过运行`dev.py`进入。

相较于普通游戏，调试模式界面右下角会出现`工具信息`和`选点坐标`。

`工具信息`：当前调试工具，取值为 `NONE`, `WALL`, `GATE`, `FOOD`, `BLINKY`, `CLYDE`, `INKY`, `PINKY`

`选点坐标`：选点在关卡地图中的坐标，左键地图时更新。坐标以左上角为`(0,0)`，横向为`x`，纵向为`y`。

调试工具使用方法：

- 使用鼠标滚轮切换当前工具，取值见上述工具信息。
- `NONE` 状态下，使用左键点击地图上的一点以选取坐标
- `WALL`/`GATE`/`FOOD` 状态下，以左键选取坐标与上次选取坐标为矩形的对角，添加对应元素。
  - `WALL` 在选定区域绘制墙体 (鬼和玩家均不可通过)。
  - `GATE` 在选定区域绘制门 (仅鬼可通过, 玩家不可通过)。
  - `FOOD` 禁止选定区域生成食物。
- `BLINKY`/`CLYDE`/`INKY`/`PINKY` 状态下，将对应鬼移动至左键点击位置。
- 在游戏界面内右键，撤销上一步操作。

> Note：暂不支持设置玩家的初始位置，请前往`assets/levels/dev.json`手动填入玩家坐标。填写格式参考`src/level.py`中`LevelData`类的注释。
>
> ~~也许后续会加这个功能？~~

完成地图的绘制后，请修改`dev.json`中的`seq`和`name`字段，并重命名该文件。

运行`main.py`时，程序将读取新的关卡数据，并按照`seq`字段升序排序进行游戏。

## 贡献者 / Contributors

![Contributors](https://contrib.rocks/image?repo=wyf7685/Pac-man)
