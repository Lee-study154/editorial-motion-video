---
name: editorial-motion-video
description: Create code-rendered social explainer and product motion videos with an editable starter, reusable approved-film components, narration/music/SFX, still-frame review, and reproducible export. Use for this editorial video workflow or adapting its film to new content.
---

# Editorial motion video

先选项目主导模式，再制作；不要把底层渲染器误称为替代用户选定 skill 的新路线。

- **解释片**：以 TalkCraft 的语义分镜与画面编排方法为主，OneTake 补充运镜、连续动作和跨尺度衔接。
- **产品宣传片**：可以 OneTake 主导；先选案例效果，核实公开源码，再决定复用或实现。Fred、ShotCraft、TalkCraft 可按镜头补充。
- **原片复现**：用打包的已验收示例；不要重新创造旧片。详见 [复现入口](references/reproduce-example.md)。

## 实际可执行入口

以本文件所在目录为 `SKILL_DIR`，脚本均不自动安装依赖或调用付费 API。

```bash
python3 "$SKILL_DIR/scripts/init_project.py" /absolute/path/new-film
python3 "$SKILL_DIR/scripts/doctor.py" /absolute/path/new-film
```

新项目编辑 `project.json`：横竖屏、帧率、色板、镜头时长、标题、素材与音轨均可替换。`public/` 存素材；`src/index.tsx` 存确定性动效。预置文字入场、页面 3D、插画浮动是轻量起点，不是 OneTake 官方案例的完整源码。预览/出片在工程目录运行 `node render.mjs --help`。

完整旧片的实际组件和素材在 `assets/attention-example.zip`，由 `init_project.py --example` 解包。包含 TalkCraft 改编页面/汇聚/文字组件、插画局部骨骼、OneTake 改编的 clearing 跨尺度结尾、已批准音轨、原创配乐源码与 4K60 快门渲染入口。

## 制作与交付

1. 明确内容与事实来源，确定旁白和分镜；镜头应解释内容，而非机械展示模板。插画比例按每个项目配置，不固定为 30%。
2. 给用户看动效选项与适用理由。OneTake 的 Films made with it 是效果案例目录，不保证每个案例完整工程已公开。每个镜头记录来源和实际采用的组件；读 [组件与三方边界](references/sources-and-boundaries.md)。
3. 真实界面素材优先来自用户提供/公开官网/演示；代码还原须忠于已核实功能，不能把重构界面说成运行实录。用户指定插画时调用其 `blue-editorial-illustrations`；没有则采用用户素材，别假定它已安装。
4. 先静帧确认构图，再以低规格检查动作、连续性与声画；配音、音乐、SFX 独立音轨，先试听，勿把原案例的合成 SFX 当成其 BGM 来源。
5. 审核遮挡、字幕、素材裁切、动效重复、音效力度、音乐与人声关系。通过后才升规格；记录分辨率、fps、时长、音轨和已知问题。

本 skill 已封装制作入口与可复现工程，尚未接入可编辑工作台。案例拆分、批准后入库等功能留到工作台阶段；不要声称已实现。
