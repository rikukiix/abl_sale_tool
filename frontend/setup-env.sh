#!/bin/bash

# 环境配置脚本
# 用于快速设置不同环境的配置文件

echo "🚀 东方Project展会出摊辅助工具 - 环境配置脚本"
echo "=================================================="

# 检查是否在frontend目录下
if [ ! -f "package.json" ]; then
    echo "❌ 请在frontend目录下运行此脚本"
    exit 1
fi

# 创建环境配置文件
create_env_file() {
    local env_type=$1
    local filename=".env.${env_type}"
    
    if [ -f "$filename" ]; then
        echo "⚠️  文件 $filename 已存在，是否覆盖？(y/N)"
        read -r response
        if [[ ! "$response" =~ ^[Yy]$ ]]; then
            echo "跳过创建 $filename"
            return
        fi
    fi
    
    case $env_type in
        "local")
            cat > "$filename" << EOF
# 开发环境配置
VITE_API_BASE_URL=/sale/api
VITE_APP_TITLE=东方Project展会出摊辅助工具 (开发版)
VITE_DEBUG_MODE=true
EOF
            ;;
        "production")
            cat > "$filename" << EOF
# 生产环境配置
VITE_API_BASE_URL=/sale/api
VITE_APP_TITLE=东方Project展会出摊辅助工具
VITE_DEBUG_MODE=false
EOF
            ;;
        "staging")
            cat > "$filename" << EOF
# 测试环境配置
VITE_API_BASE_URL=/sale/api
VITE_APP_TITLE=东方Project展会出摊辅助工具 (测试版)
VITE_DEBUG_MODE=true
EOF
            ;;
    esac
    
    echo "✅ 已创建 $filename"
}

# 显示当前配置
show_current_config() {
    echo ""
    echo "📋 当前环境配置："
    echo "=================="
    
    if [ -f ".env.local" ]; then
        echo "🔧 开发环境 (.env.local):"
        cat .env.local | grep -v "^#" | grep -v "^$" || echo "  (无配置)"
    else
        echo "🔧 开发环境 (.env.local): 未配置"
    fi
    
    if [ -f ".env.production" ]; then
        echo ""
        echo "🚀 生产环境 (.env.production):"
        cat .env.production | grep -v "^#" | grep -v "^$" || echo "  (无配置)"
    else
        echo ""
        echo "🚀 生产环境 (.env.production): 未配置"
    fi
    
    if [ -f ".env.staging" ]; then
        echo ""
        echo "🧪 测试环境 (.env.staging):"
        cat .env.staging | grep -v "^#" | grep -v "^$" || echo "  (无配置)"
    fi
}

# 主菜单
main_menu() {
    echo ""
    echo "请选择操作："
    echo "1) 创建开发环境配置 (.env.local)"
    echo "2) 创建生产环境配置 (.env.production)"
    echo "3) 创建测试环境配置 (.env.staging)"
    echo "4) 显示当前配置"
    echo "5) 创建所有环境配置"
    echo "6) 退出"
    echo ""
    echo "请输入选项 (1-6):"
    
    read -r choice
    
    case $choice in
        1)
            create_env_file "local"
            ;;
        2)
            create_env_file "production"
            ;;
        3)
            create_env_file "staging"
            ;;
        4)
            show_current_config
            ;;
        5)
            create_env_file "local"
            create_env_file "production"
            create_env_file "staging"
            ;;
        6)
            echo "👋 再见！"
            exit 0
            ;;
        *)
            echo "❌ 无效选项，请重新选择"
            main_menu
            ;;
    esac
}

# 显示帮助信息
show_help() {
    echo ""
    echo "📖 使用说明："
    echo "============="
    echo "• 此脚本用于快速创建不同环境的配置文件"
    echo "• 开发环境 (.env.local): 用于本地开发，包含调试信息"
    echo "• 生产环境 (.env.production): 用于生产部署，关闭调试功能"
    echo "• 测试环境 (.env.staging): 用于测试环境，开启调试功能"
    echo ""
    echo "🔧 环境变量说明："
    echo "=================="
    echo "• VITE_API_BASE_URL: API基础路径，默认为 /sale/api"
    echo "• VITE_APP_TITLE: 应用标题"
    echo "• VITE_DEBUG_MODE: 调试模式开关"
    echo ""
    echo "📁 文件位置："
    echo "============="
    echo "• 配置文件将创建在 frontend 目录下"
    echo "• 参考文档：frontend/ENV_CONFIG.md"
}

# 检查命令行参数
if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    show_help
    exit 0
fi

# 显示帮助信息
show_help

# 显示当前配置
show_current_config

# 进入主菜单
main_menu

echo ""
echo "🎉 环境配置完成！"
echo "📖 更多配置说明请查看 frontend/ENV_CONFIG.md"
