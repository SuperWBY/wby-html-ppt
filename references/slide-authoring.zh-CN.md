# 页面制作

[English](slide-authoring.md) | 中文

## 源文件与叙事

`deck.json` 是唯一页面顺序清单，`slides/*.html` 是可编辑页面，素材放在项目内。大纲代表意图，不代表页面已完成。修改源页面，不修改生成的预览产物。

每页先明确展示对象、观众需要理解的内容、支撑它的证据或画面，以及缺失事实。演示产品时说明操作发生在哪里、结果出现在哪里；只有讲解实现时才突出内部名称。

每页聚焦一个主要信息。内容过多时按主题或过程拆页，保留必要的原因、影响、条件和操作；相邻页重复时可以合并。局部修改保留已确认内容。用户已授权整套制作时，不逐页索要许可。

## 构图与实现

根据内容选择聚焦、对照、顺序、汇聚、证据或变化等构图，不要求固定数量。有层级的内容不要反复排成等权卡片。

建立一致的字体、配色、间距和插画媒介基准。字号由投影和观看条件决定，不能靠整体缩小文字解决内容过多。图像已经表达的信息，不在标题、图注和正文反复重述。

单页样式隔离。随附播放器适配 1920×1080 画布；更改画布时同步修改播放器尺寸计算。保持图片比例与截图必要上下文。精确文字和关系用代码，场景用生图；教学示意与真实证据要区分。

## 内置命令

将 scripts/deck.py 解析为本 Skill 下的绝对路径。只需 Python 3.9+，不需要 oil-ppt 命令或其他 Skill。

```sh
python3 scripts/deck.py init /path/to/deck --title "演示标题"
python3 scripts/deck.py add /path/to/deck opening --title "开场"
python3 scripts/deck.py add /path/to/deck evidence --title "证据" --after opening
python3 scripts/deck.py move /path/to/deck evidence --to 1
python3 scripts/deck.py remove /path/to/deck evidence
python3 scripts/deck.py status /path/to/deck
python3 scripts/deck.py check /path/to/deck
python3 scripts/deck.py build /path/to/deck --output /path/to/deck/dist/talk.html
python3 scripts/deck.py preview /path/to/deck --port 4173
```

add 只创建待制作画布。完成制作后删除 data-wby-draft 标记；check/build/preview 会拒绝仍带标记的草稿。ID 使用小写字母、数字和连字符。排序位置从 1 开始。remove 只移出清单，保留源文件和素材；清单更新前保存 deck.json.bak。恢复页面时把原路径重新加入清单，不覆盖原文件。

status 报告文件、标题和草稿状态；check 在临时目录验证静态打包，不证明视觉质量。preview 构建后仅在本机提供输出目录的预览服务，Ctrl+C 停止；使用独立输出目录。修改后需重新构建，没有自动刷新；端口占用时选择另一端口。

## 检查

文案参考 [copywriting.zh-CN.md](copywriting.zh-CN.md)，视觉参考 [visual-method.md](visual-method.md)。浏览器检查裁切、滚动、重叠、对比度、投影可读性、缺失素材和连续重复构图。最终文件按 [interaction-delivery.md](interaction-delivery.md) 验收；静态检查不能替代浏览器检查。
