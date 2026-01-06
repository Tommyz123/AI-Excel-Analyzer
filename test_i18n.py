#!/usr/bin/env python3
"""
国际化（i18n）配置检查脚本

用途：
- 验证 UI_TEXT_EN 和 UI_TEXT_ZH 的键是否完全匹配
- 检查占位符是否一致
- 生成测试报告

运行方法：
    python3 test_i18n.py
"""

import re
from config import UI_TEXT_EN, UI_TEXT_ZH


def check_keys():
    """检查中英文键是否匹配"""
    print("=" * 60)
    print("1. 检查键值对匹配...")
    print("=" * 60)

    en_keys = set(UI_TEXT_EN.keys())
    zh_keys = set(UI_TEXT_ZH.keys())

    missing_in_zh = en_keys - zh_keys
    missing_in_en = zh_keys - en_keys

    if not missing_in_zh and not missing_in_en:
        print("✅ 所有键完全匹配！")
        print(f"   共有 {len(en_keys)} 个键值对")
        return True
    else:
        if missing_in_zh:
            print(f"❌ 中文缺少 {len(missing_in_zh)} 个键：")
            for key in sorted(missing_in_zh):
                print(f"   - {key}")

        if missing_in_en:
            print(f"❌ 英文缺少 {len(missing_in_en)} 个键：")
            for key in sorted(missing_in_en):
                print(f"   - {key}")

        return False


def check_placeholders():
    """检查占位符是否匹配"""
    print("\n" + "=" * 60)
    print("2. 检查占位符匹配...")
    print("=" * 60)

    en_keys = set(UI_TEXT_EN.keys())
    zh_keys = set(UI_TEXT_ZH.keys())
    common_keys = en_keys & zh_keys

    errors = []

    for key in sorted(common_keys):
        en_text = str(UI_TEXT_EN[key])
        zh_text = str(UI_TEXT_ZH[key])

        # 提取占位符（如 {date}, {amount}, {pct}）
        en_placeholders = set(re.findall(r'\{(\w+)', en_text))
        zh_placeholders = set(re.findall(r'\{(\w+)', zh_text))

        if en_placeholders != zh_placeholders:
            errors.append({
                'key': key,
                'en_placeholders': en_placeholders,
                'zh_placeholders': zh_placeholders
            })

    if not errors:
        print("✅ 所有占位符完全匹配！")
        return True
    else:
        print(f"⚠️  发现 {len(errors)} 个占位符不匹配：\n")
        for error in errors:
            print(f"键：{error['key']}")
            print(f"  英文占位符：{error['en_placeholders']}")
            print(f"  中文占位符：{error['zh_placeholders']}")
            print()
        return False


def check_text_types():
    """检查文本类型是否一致"""
    print("=" * 60)
    print("3. 检查文本类型...")
    print("=" * 60)

    en_keys = set(UI_TEXT_EN.keys())
    zh_keys = set(UI_TEXT_ZH.keys())
    common_keys = en_keys & zh_keys

    errors = []

    for key in common_keys:
        en_val = UI_TEXT_EN[key]
        zh_val = UI_TEXT_ZH[key]

        # 检查类型是否相同
        if type(en_val) != type(zh_val):
            errors.append({
                'key': key,
                'en_type': type(en_val).__name__,
                'zh_type': type(zh_val).__name__
            })

    if not errors:
        print("✅ 所有文本类型一致！")
        return True
    else:
        print(f"❌ 发现 {len(errors)} 个类型不匹配：")
        for error in errors:
            print(f"  {error['key']}: EN={error['en_type']}, ZH={error['zh_type']}")
        return False


def generate_statistics():
    """生成统计信息"""
    print("\n" + "=" * 60)
    print("4. 统计信息")
    print("=" * 60)

    en_keys = UI_TEXT_EN.keys()

    # 按前缀分类
    categories = {}
    for key in en_keys:
        prefix = key.split('_')[0]
        categories[prefix] = categories.get(prefix, 0) + 1

    print(f"\n总键值对数：{len(en_keys)}\n")
    print("按前缀分类：")
    for prefix, count in sorted(categories.items(), key=lambda x: -x[1]):
        print(f"  {prefix:30s}: {count:3d} 个")

    # 统计包含占位符的键
    placeholder_count = 0
    for key in en_keys:
        if '{' in str(UI_TEXT_EN[key]):
            placeholder_count += 1

    print(f"\n包含占位符的键：{placeholder_count} 个")
    print(f"纯文本的键：{len(en_keys) - placeholder_count} 个")


def main():
    """主函数"""
    print("\n🌐 国际化配置检查工具")
    print("=" * 60)
    print("检查 config.py 中的 UI_TEXT_EN 和 UI_TEXT_ZH")
    print("=" * 60 + "\n")

    # 运行所有检查
    results = []
    results.append(("键匹配", check_keys()))
    results.append(("占位符匹配", check_placeholders()))
    results.append(("类型一致", check_text_types()))

    # 生成统计
    generate_statistics()

    # 总结
    print("\n" + "=" * 60)
    print("📋 检查总结")
    print("=" * 60)

    all_passed = all(result[1] for result in results)

    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"  {name:20s}: {status}")

    print("\n" + "=" * 60)

    if all_passed:
        print("🎉 所有检查通过！国际化配置正确。")
        print("=" * 60)
        return 0
    else:
        print("⚠️  发现问题，请修复后重新运行。")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    exit(main())
