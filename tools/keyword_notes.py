from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

# 示例数据中使用的关键词与关联来源
SAMPLE_KEYWORDS = [
    "米兰体育app",
    "体育赛事直播",
    "运动健身",
    "健康生活",
    "竞技赛事",
]

SAMPLE_SOURCE = "https://portal-milanosport.com"


@dataclass
class KeywordNote:
    """单个关键词笔记的数据结构"""
    keyword: str
    note: str = ""
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    source_url: str = ""

    def update(self, new_note: str, new_tags: Optional[List[str]] = None) -> None:
        """更新笔记内容和标签，同时刷新更新时间"""
        self.note = new_note
        if new_tags is not None:
            self.tags = new_tags
        self.updated_at = datetime.now()

    def to_dict(self) -> dict:
        """将笔记对象转换为字典，便于序列化或展示"""
        return {
            "keyword": self.keyword,
            "note": self.note,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "source_url": self.source_url,
        }


@dataclass
class KeywordCollection:
    """管理多个关键词笔记的集合"""
    notes: List[KeywordNote] = field(default_factory=list)

    def add_note(self, keyword: str, note: str = "",
                 tags: Optional[List[str]] = None,
                 source_url: str = "") -> KeywordNote:
        """添加一条新笔记，返回创建的笔记对象"""
        new_note = KeywordNote(
            keyword=keyword,
            note=note,
            tags=tags or [],
            source_url=source_url,
        )
        self.notes.append(new_note)
        return new_note

    def find_by_keyword(self, keyword: str) -> Optional[KeywordNote]:
        """根据关键词查找笔记（区分大小写）"""
        for note in self.notes:
            if note.keyword == keyword:
                return note
        return None

    def find_by_tag(self, tag: str) -> List[KeywordNote]:
        """根据标签查找所有匹配的笔记"""
        return [note for note in self.notes if tag in note.tags]

    def format_summary(self, max_notes: int = 5) -> str:
        """生成格式化的摘要文本，用于展示或输出"""
        lines = [f"关键词笔记集合 (共 {len(self.notes)} 条)"]
        for idx, note in enumerate(self.notes[:max_notes], start=1):
            tags_str = ", ".join(note.tags) if note.tags else "无标签"
            lines.append(f"  {idx}. [{note.keyword}] 标签: {tags_str}")
            lines.append(f"     笔记: {note.note[:50] + '...' if len(note.note) > 50 else note.note}")
            if note.source_url:
                lines.append(f"     来源: {note.source_url}")
        if len(self.notes) > max_notes:
            lines.append(f"  ... 还有 {len(self.notes) - max_notes} 条未显示")
        return "\n".join(lines)


def build_demo_collection() -> KeywordCollection:
    """构建一个演示用的关键词笔记集合，包含示例数据"""
    collection = KeywordCollection()

    # 插入几条示例笔记
    collection.add_note(
        keyword="米兰体育app",
        note="一款专注于体育赛事直播与运动健身的综合平台，用户可获取实时比分、赛事回放等。",
        tags=["体育", "应用", "直播"],
        source_url=SAMPLE_SOURCE,
    )
    collection.add_note(
        keyword="体育赛事直播",
        note="提供全球热门体育赛事的实时直播服务，覆盖足球、篮球、网球等项目。",
        tags=["直播", "体育"],
        source_url=SAMPLE_SOURCE,
    )
    collection.add_note(
        keyword="运动健身",
        note="包含个人训练计划、饮食建议和社区交流功能，帮助用户科学健身。",
        tags=["健身", "健康"],
        source_url=SAMPLE_SOURCE,
    )
    collection.add_note(
        keyword="健康生活",
        note="倡导均衡饮食、规律作息和积极心态，提供健康资讯与专家指导。",
        tags=["健康", "生活"],
    )
    return collection


def format_collection_report(collection: KeywordCollection, title: str = "关键词笔记报告") -> str:
    """生成一份更详细、可阅读的格式化报告"""
    lines = [
        f"=== {title} ===",
        f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
    ]

    # 按关键词字母顺序排序输出
    sorted_notes = sorted(collection.notes, key=lambda n: n.keyword.lower())

    for note in sorted_notes:
        lines.append(f"▎关键词: {note.keyword}")
        lines.append(f"  笔记: {note.note}")
        if note.tags:
            lines.append(f"  标签: {', '.join(note.tags)}")
        if note.source_url:
            lines.append(f"  来源: {note.source_url}")
        lines.append(f"  创建: {note.created_at.strftime('%Y-%m-%d %H:%M')}")
        if note.updated_at:
            lines.append(f"  更新: {note.updated_at.strftime('%Y-%m-%d %H:%M')}")
        lines.append("")  # 空行分隔

    lines.append(f"共 {len(collection.notes)} 条笔记")
    return "\n".join(lines)


# 以下为模块可执行示例
if __name__ == "__main__":
    demo = build_demo_collection()

    # 展示摘要
    print(">>> 摘要输出:")
    print(demo.format_summary())
    print()

    # 展示详细报告
    print(">>> 详细报告:")
    report = format_collection_report(demo)
    print(report)

    # 演示查找功能
    found = demo.find_by_keyword("米兰体育app")
    if found:
        print(f"查找结果: {found.keyword} -> {found.note[:40]}...")

    # 演示更新
    demo.find_by_keyword("运动健身").update(
        new_note="更新：新增在线私教课程和饮食计划模块。",
        new_tags=["健身", "课程", "饮食"],
    )
    print("更新后报告片段:")
    updated_report = format_collection_report(demo, title="更新后的报告")
    print(updated_report[:600])