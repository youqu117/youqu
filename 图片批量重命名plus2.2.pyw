import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import tempfile
from datetime import datetime
import re

def natural_sort_key(filename):
    """
    自然排序键函数，确保数字按数值大小排序
    例如：1, 2, 10, 11 而不是 1, 10, 11, 2
    """
    return [int(text) if text.isdigit() else text.lower() 
            for text in re.split(r'(\d+)', filename)]

class ImprovedImageRenamer:
    def __init__(self, root):
        self.root = root
        self.root.title("高级图片批量重命名工具")
        self.root.geometry("900x750")  # 稍微增加宽度以容纳更多内容
        self.root.configure(bg='#f5f5f5')
        
        # 设置样式
        self.setup_styles()
        
        # 初始化变量
        self.mode_var = tk.StringVar(value="single")  # 默认单一序列模式
        self.prefix_var = tk.StringVar(value="")
        self.format_var = tk.StringVar(value="{num:03d}")  # 默认三位数字编号
        
        # 文件类型变量
        self.file_types_var = tk.StringVar(value=".jpg;.jpeg;.png;.gif;.bmp;.tiff;.webp;.tif;.heic;.svg")
        self.input_dir_var = tk.StringVar(value=os.getcwd())
        self.output_dir_var = tk.StringVar(value=os.getcwd())
        
        # x-y格式专用变量
        self.x_start_var = tk.IntVar(value=1)
        self.y_start_var = tk.IntVar(value=1)
        self.x_max_var = tk.IntVar(value=5)
        self.y_max_var = tk.IntVar(value=5)
        
        # 单一序列格式专用变量
        self.start_num_var = tk.IntVar(value=1)
        
        # 存储文件列表
        self.image_files = []
        
        self.setup_ui()

    def setup_styles(self):
        """设置样式"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 配置样式
        style.configure('Title.TLabel', font=('微软雅黑', 16, 'bold'), foreground='#2c3e50')
        style.configure('Section.TLabelframe.Label', font=('微软雅黑', 10, 'bold'), foreground='#34495e')
        style.configure('Section.TLabelframe', relief='solid', borderwidth=1)
        style.configure('Action.TButton', font=('微软雅黑', 9, 'bold'))
        style.configure('Success.TLabel', foreground='#27ae60')
        style.configure('Warning.TLabel', foreground='#e74c3c')
        
        # 状态栏样式
        style.configure('Status.TLabel', font=('微软雅黑', 9), foreground='#7f8c8d', background='#ecf0f1')
        
        # Treeview样式
        style.configure('Custom.Treeview', font=('微软雅黑', 9))
        style.configure('Custom.Treeview.Heading', font=('微软雅黑', 9, 'bold'))

    def setup_ui(self):
        """设置用户界面，使用grid布局管理器确保整齐排列"""
        # 主容器
        main_container = ttk.Frame(self.root, padding="0")
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 标题区域
        title_frame = ttk.Frame(main_container, style='Title.TFrame')
        title_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        
        title_label = ttk.Label(title_frame, text="📷 图片批量重命名工具", 
                               style='Title.TLabel')
        title_label.pack(pady=10)
        
        # 左侧面板 - 设置区域
        left_panel = ttk.Frame(main_container)
        left_panel.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        
        # 右侧面板 - 文件列表和操作区域
        right_panel = ttk.Frame(main_container)
        right_panel.grid(row=1, column=1, sticky="nsew")
        
        # 调整列权重，确保左右面板比例合适
        main_container.columnconfigure(0, weight=1)
        main_container.columnconfigure(1, weight=1)
        main_container.rowconfigure(1, weight=1)
        
        # === 左侧面板内容 ===
        
        # 文件夹设置框架
        dir_frame = ttk.LabelFrame(left_panel, text="📁 文件夹设置", padding="12", style='Section.TLabelframe')
        dir_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 输入文件夹
        ttk.Label(dir_frame, text="输入文件夹:", font=('微软雅黑', 9)).grid(row=0, column=0, sticky="w", pady=(0, 5))
        input_entry = ttk.Entry(dir_frame, textvariable=self.input_dir_var, font=('微软雅黑', 9))
        input_entry.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        ttk.Button(dir_frame, text="浏览...", command=self.select_input_dir, width=8).grid(row=1, column=1, padx=(5, 0))
        
        # 输出文件夹
        ttk.Label(dir_frame, text="输出文件夹:", font=('微软雅黑', 9)).grid(row=2, column=0, sticky="w", pady=(5, 5))
        output_entry = ttk.Entry(dir_frame, textvariable=self.output_dir_var, font=('微软雅黑', 9))
        output_entry.grid(row=3, column=0, sticky="ew", pady=(0, 5))
        ttk.Button(dir_frame, text="浏览...", command=self.select_output_dir, width=8).grid(row=3, column=1, padx=(5, 0))
        
        dir_frame.columnconfigure(0, weight=1)
        
        # 文件类型设置框架
        filetype_frame = ttk.LabelFrame(left_panel, text="🔧 文件类型设置", padding="12", style='Section.TLabelframe')
        filetype_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(filetype_frame, text="支持的文件扩展名:", font=('微软雅黑', 9)).grid(row=0, column=0, sticky="w")
        filetype_entry = ttk.Entry(filetype_frame, textvariable=self.file_types_var, font=('微软雅黑', 9))
        filetype_entry.grid(row=1, column=0, sticky="ew", pady=(5, 0))
        
        # 提示文字
        hint_label = ttk.Label(filetype_frame, 
                             text="多个扩展名用分号分隔，例如: .jpg;.png;.gif", 
                             font=('微软雅黑', 8), foreground='#e74c3c')
        hint_label.grid(row=2, column=0, sticky="w", pady=(2, 0))
        
        filetype_frame.columnconfigure(0, weight=1)
        
        # 重命名模式框架
        mode_frame = ttk.LabelFrame(left_panel, text="⚙️ 重命名模式", padding="12", style='Section.TLabelframe')
        mode_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 模式选择
        mode_inner_frame = ttk.Frame(mode_frame)
        mode_inner_frame.pack(fill=tk.X, pady=5)
        
        ttk.Radiobutton(mode_inner_frame, text="单一数字序列", variable=self.mode_var, 
                       value="single", command=self.toggle_mode).pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(mode_inner_frame, text="X-Y矩阵格式", variable=self.mode_var, 
                       value="xy", command=self.toggle_mode).pack(side=tk.LEFT)
        
        # 通用设置框架
        common_frame = ttk.LabelFrame(left_panel, text="🔠 通用设置", padding="12", style='Section.TLabelframe')
        common_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 前缀和格式设置
        prefix_frame = ttk.Frame(common_frame)
        prefix_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(prefix_frame, text="文件前缀:", font=('微软雅黑', 9)).pack(side=tk.LEFT)
        ttk.Entry(prefix_frame, textvariable=self.prefix_var, width=15, font=('微软雅黑', 9)).pack(side=tk.LEFT, padx=(5, 20))
        
        ttk.Label(prefix_frame, text="编号格式:", font=('微软雅黑', 9)).pack(side=tk.LEFT)
        format_combo = ttk.Combobox(prefix_frame, textvariable=self.format_var, width=12,
                                   values=["{num}", "{num:02d}", "{num:03d}", "{num:04d}"],
                                   state="readonly", font=('微软雅黑', 9))
        format_combo.pack(side=tk.LEFT, padx=5)
        format_combo.set("{num:03d}")
        
        # 单一序列设置框架
        self.single_frame = ttk.LabelFrame(left_panel, text="🔢 单一序列设置", padding="12", style='Section.TLabelframe')
        self.single_frame.pack(fill=tk.X, pady=(0, 10))
        
        single_inner = ttk.Frame(self.single_frame)
        single_inner.pack(fill=tk.X, pady=5)
        
        ttk.Label(single_inner, text="起始编号:", font=('微软雅黑', 9)).pack(side=tk.LEFT)
        ttk.Spinbox(single_inner, from_=1, to=9999, textvariable=self.start_num_var, 
                   width=10, font=('微软雅黑', 9)).pack(side=tk.LEFT, padx=5)
        
        # X-Y格式设置框架
        self.xy_frame = ttk.LabelFrame(left_panel, text="📊 X-Y矩阵设置", padding="12", style='Section.TLabelframe')
        self.xy_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 第一行：X和Y起始值
        xy_row1 = ttk.Frame(self.xy_frame)
        xy_row1.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Label(xy_row1, text="X起始值:", font=('微软雅黑', 9)).pack(side=tk.LEFT)
        ttk.Spinbox(xy_row1, from_=1, to=999, textvariable=self.x_start_var, 
                   width=8, font=('微软雅黑', 9)).pack(side=tk.LEFT, padx=(5, 15))
        
        ttk.Label(xy_row1, text="Y起始值:", font=('微软雅黑', 9)).pack(side=tk.LEFT)
        ttk.Spinbox(xy_row1, from_=1, to=999, textvariable=self.y_start_var, 
                   width=8, font=('微软雅黑', 9)).pack(side=tk.LEFT, padx=5)
        
        # 第二行：X和Y最大值
        xy_row2 = ttk.Frame(self.xy_frame)
        xy_row2.pack(fill=tk.X, pady=(8, 5))
        
        ttk.Label(xy_row2, text="X最大值-1:", font=('微软雅黑', 9)).pack(side=tk.LEFT)
        ttk.Spinbox(xy_row2, from_=1, to=999, textvariable=self.x_max_var, 
                   width=8, font=('微软雅黑', 9)).pack(side=tk.LEFT, padx=(5, 15))
        
        ttk.Label(xy_row2, text="Y最大值-1:", font=('微软雅黑', 9)).pack(side=tk.LEFT)
        ttk.Spinbox(xy_row2, from_=1, to=999, textvariable=self.y_max_var, 
                   width=8, font=('微软雅黑', 9)).pack(side=tk.LEFT, padx=5)
        
        # === 右侧面板内容 ===
        
        # 文件列表框架
        list_frame = ttk.LabelFrame(right_panel, text="📄 检测到的文件", padding="12", style='Section.TLabelframe')
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 选择按钮框架
        select_btn_frame = ttk.Frame(list_frame)
        select_btn_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Button(select_btn_frame, text="✅ 全选", command=self.select_all, width=8).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(select_btn_frame, text="❌ 取消全选", command=self.deselect_all, width=10).pack(side=tk.LEFT)
        
        # 文件列表和滚动条
        list_container = ttk.Frame(list_frame)
        list_container.pack(fill=tk.BOTH, expand=True)
        
        # 创建Treeview代替Listbox
        self.file_tree = ttk.Treeview(list_container, columns=("selected", "filename"), 
                                     show=("headings"), height=15, style='Custom.Treeview')
        
        # 设置列
        self.file_tree.heading("selected", text="选择")
        self.file_tree.heading("filename", text="文件名")
        self.file_tree.column("selected", width=60, anchor="center", minwidth=60)
        self.file_tree.column("filename", width=400, anchor="w", minwidth=200)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(list_container, orient=tk.VERTICAL, command=self.file_tree.yview)
        self.file_tree.configure(yscrollcommand=scrollbar.set)
        
        self.file_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 绑定复选框点击事件
        self.file_tree.bind("<Button-1>", self.on_tree_click)
        
        # 操作按钮框架
        button_frame = ttk.LabelFrame(right_panel, text="🚀 操作", padding="12", style='Section.TLabelframe')
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 按钮容器
        btn_container = ttk.Frame(button_frame)
        btn_container.pack(fill=tk.X)
        
        ttk.Button(btn_container, text="🔄 刷新文件列表", 
                  command=self.refresh_file_list, style='Action.TButton').pack(side=tk.LEFT, padx=(0, 5), expand=True, fill=tk.X)
        ttk.Button(btn_container, text="👁️ 预览重命名结果", 
                  command=self.preview_rename, style='Action.TButton').pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        ttk.Button(btn_container, text="✅ 执行重命名", 
                  command=self.execute_rename, style='Action.TButton').pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        ttk.Button(btn_container, text="❌ 退出程序", 
                  command=self.root.quit, style='Action.TButton').pack(side=tk.LEFT, padx=(5, 0), expand=True, fill=tk.X)
        
        # 状态栏
        status_frame = ttk.Frame(right_panel, relief='solid', borderwidth=1)
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.status_var = tk.StringVar(value="就绪 - 请选择输入文件夹并刷新文件列表")
        status_bar = ttk.Label(status_frame, textvariable=self.status_var, 
                              style='Status.TLabel', padding=(10, 5))
        status_bar.pack(fill=tk.X)
        
        # 操作指南
        help_frame = ttk.LabelFrame(right_panel, text="💡 使用指南", padding="10", style='Section.TLabelframe')
        help_frame.pack(fill=tk.X)
        
        help_text = """1. 设置输入/输出文件夹
2. 选择重命名模式（单一序列或X-Y矩阵）
3. 设置文件前缀和编号格式
4. 点击"刷新文件列表"查看文件
5. 选择要重命名的文件（默认全选）
6. 预览结果后执行重命名"""
        
        help_label = ttk.Label(help_frame, text=help_text, font=('微软雅黑', 9), 
                              justify=tk.LEFT, background='#f8f9fa')
        help_label.pack(fill=tk.X)
        
        # 初始模式切换和文件列表加载
        self.toggle_mode()
        self.refresh_file_list()

    def on_tree_click(self, event):
        """处理Treeview点击事件，实现复选框功能"""
        item = self.file_tree.identify_row(event.y)
        column = self.file_tree.identify_column(event.x)
        
        if item and column == "#1":  # 点击了选择列
            current_values = self.file_tree.item(item, "values")
            if current_values:
                # 切换选择状态
                new_selected = "❌" if current_values[0] == "✅" else "✅"
                self.file_tree.set(item, "selected", new_selected)
                
                # 更新状态显示
                self.update_selection_status()

    def select_all(self):
        """全选所有文件"""
        for item in self.file_tree.get_children():
            self.file_tree.set(item, "selected", "✅")
        self.update_selection_status()

    def deselect_all(self):
        """取消全选所有文件"""
        for item in self.file_tree.get_children():
            self.file_tree.set(item, "selected", "❌")
        self.update_selection_status()

    def update_selection_status(self):
        """更新选择状态显示"""
        total_count = len(self.file_tree.get_children())
        selected_count = sum(1 for item in self.file_tree.get_children() 
                           if self.file_tree.set(item, "selected") == "✅")
        
        file_extensions = self.get_file_extensions()
        self.status_var.set(f"✅ 找到 {total_count} 个文件，已选择 {selected_count} 个（类型: {', '.join(file_extensions)}）")

    def get_selected_files(self):
        """获取选中的文件列表"""
        selected_files = []
        for item in self.file_tree.get_children():
            if self.file_tree.set(item, "selected") == "✅":
                filename = self.file_tree.set(item, "filename")
                selected_files.append(filename)
        return selected_files

    def select_input_dir(self):
        """选择输入文件夹"""
        directory = filedialog.askdirectory(initialdir=self.input_dir_var.get(), title="选择输入文件夹")
        if directory:
            self.input_dir_var.set(directory)
            self.refresh_file_list()

    def select_output_dir(self):
        """选择输出文件夹"""
        directory = filedialog.askdirectory(initialdir=self.output_dir_var.get(), title="选择输出文件夹")
        if directory:
            self.output_dir_var.set(directory)

    def toggle_mode(self):
        """切换显示模式对应的设置面板"""
        if self.mode_var.get() == "single":
            self.single_frame.pack(fill=tk.X, pady=(0, 10))  # 显示单一序列设置
            self.xy_frame.pack_forget()  # 隐藏X-Y矩阵设置
        else:
            self.single_frame.pack_forget()  # 隐藏单一序列设置
            self.xy_frame.pack(fill=tk.X, pady=(0, 10))  # 显示X-Y矩阵设置

    def get_file_extensions(self):
        """从输入框获取文件扩展名列表"""
        extensions_str = self.file_types_var.get().strip()
        if not extensions_str:
            return ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
        
        # 分割扩展名，清理空格，确保以点开头
        extensions = []
        for ext in extensions_str.split(';'):
            ext = ext.strip()
            if ext and not ext.startswith('.'):
                ext = '.' + ext
            if ext:
                extensions.append(ext.lower())
        
        return extensions if extensions else ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']

    def refresh_file_list(self):
        """刷新文件列表"""
        input_dir = self.input_dir_var.get()
        if not os.path.exists(input_dir):
            messagebox.showerror("错误", f"输入文件夹不存在: {input_dir}")
            return
        
        file_extensions = self.get_file_extensions()
        
        # 清空Treeview
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
        
        try:
            self.image_files = []
            for file in os.listdir(input_dir):
                file_lower = file.lower()
                if any(file_lower.endswith(ext) for ext in file_extensions):
                    self.image_files.append(file)
            
            if not self.image_files:
                self.file_tree.insert("", "end", values=("", f"未找到指定类型的文件（{', '.join(file_extensions)}）"))
                self.status_var.set(f"⚠️ 警告: 当前文件夹中没有找到指定类型的文件")
                return
            
            # 自然排序
            self.image_files.sort(key=natural_sort_key)
            
            # 插入文件到Treeview，默认全选
            for file in self.image_files:
                self.file_tree.insert("", "end", values=("✅", file))
                
            self.update_selection_status()
            
        except Exception as e:
            messagebox.showerror("错误", f"读取文件列表时出错: {str(e)}")
            self.status_var.set("❌ 错误: 无法读取文件列表")

    def generate_rename_plan(self):
        """生成重命名计划"""
        input_dir = self.input_dir_var.get()
        output_dir = self.output_dir_var.get()
        
        if not os.path.exists(input_dir):
            messagebox.showerror("错误", f"输入文件夹不存在: {input_dir}")
            return None
        
        if not os.path.exists(output_dir):
            # 尝试创建输出文件夹
            try:
                os.makedirs(output_dir)
            except Exception as e:
                messagebox.showerror("错误", f"无法创建输出文件夹: {str(e)}")
                return None
        
        # 获取选中的文件
        selected_files = self.get_selected_files()
        
        if not selected_files:
            messagebox.showwarning("警告", "请先选择要重命名的文件！")
            return None
        
        # 使用选中的文件列表
        image_files = selected_files
        
        if not image_files:
            file_extensions = self.get_file_extensions()
            messagebox.showwarning("警告", f"当前文件夹中没有找到指定类型的文件（{', '.join(file_extensions)}）！")
            return None
        
        # 生成重命名计划
        rename_plan = []
        prefix = self.prefix_var.get().strip()
        
        if self.mode_var.get() == "single":
            # 单一序列模式
            start_num = self.start_num_var.get()
            format_template = self.format_var.get()
            
            for i, old_name in enumerate(image_files):
                _, ext = os.path.splitext(old_name)
                current_num = start_num + i
                
                # 应用格式模板
                try:
                    if "{num" in format_template:
                        new_name = format_template.format(num=current_num) + ext
                    else:
                        new_name = f"{current_num}{ext}"
                except:
                    new_name = f"{current_num}{ext}"
                
                # 添加前缀
                if prefix and not new_name.startswith(prefix):
                    new_name = prefix + new_name
                    
                rename_plan.append((old_name, new_name))
        else:
            # X-Y矩阵模式
            x_start = self.x_start_var.get()
            y_start = self.y_start_var.get()
            x_max = self.x_max_var.get()
            y_max = self.y_max_var.get()
            
            for i, old_name in enumerate(image_files):
                _, ext = os.path.splitext(old_name)
                
                # 计算x和y的值（考虑起始值）
                x_val = x_start + (i // y_max)
                y_val = y_start + (i % y_max)
                
                # 如果x值超出范围，停止处理
                if x_val > x_start + x_max - 1:
                    break
                
                new_name = f"{x_val}-{y_val}{ext}"
                
                # 添加前缀
                if prefix and not new_name.startswith(prefix):
                    new_name = prefix + new_name
                    
                rename_plan.append((old_name, new_name))
        
        return rename_plan

    def preview_rename(self):
        """预览重命名结果"""
        rename_plan = self.generate_rename_plan()
        if not rename_plan:
            return
            
        # 创建预览窗口
        preview_window = tk.Toplevel(self.root)
        preview_window.title("重命名预览")
        preview_window.geometry("700x500")
        preview_window.transient(self.root)
        preview_window.grab_set()
        
        # 居中显示
        preview_window.update_idletasks()
        x = (preview_window.winfo_screenwidth() // 2) - (700 // 2)
        y = (preview_window.winfo_screenheight() // 2) - (500 // 2)
        preview_window.geometry(f"+{x}+{y}")
        
        preview_frame = ttk.Frame(preview_window, padding="15")
        preview_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(preview_frame, text="🔍 重命名预览（执行前请仔细核对）", 
                 font=("微软雅黑", 12, "bold")).pack(pady=(0, 10))
        
        # 显示输入输出路径
        path_frame = ttk.Frame(preview_frame)
        path_frame.pack(fill=tk.X, pady=(0, 10))
        
        path_info = f"📁 输入文件夹: {self.input_dir_var.get()}\n📁 输出文件夹: {self.output_dir_var.get()}\n"
        path_label = ttk.Label(path_frame, text=path_info, font=("微软雅黑", 9), justify=tk.LEFT)
        path_label.pack(anchor=tk.W)
        
        # 创建文本框显示预览
        text_frame = ttk.LabelFrame(preview_frame, text="重命名详情", padding="5")
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        text_widget = tk.Text(text_frame, width=70, height=20, font=("Consolas", 9))
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 填充预览信息
        preview_text = "以下是将要执行的重命名操作：\n" + "="*50 + "\n\n"
        for i, (old_name, new_name) in enumerate(rename_plan, 1):
            preview_text += f"{i:2d}. {old_name}\n    → {new_name}\n"
        
        preview_text += f"\n" + "="*50 + f"\n总计: {len(rename_plan)} 个文件"
        text_widget.insert(tk.END, preview_text)
        text_widget.config(state=tk.DISABLED)
        
        # 按钮框架
        btn_frame = ttk.Frame(preview_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(btn_frame, text="✅ 确认并执行", 
                  command=lambda: [preview_window.destroy(), self.execute_rename()]).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(btn_frame, text="❌ 关闭", 
                  command=preview_window.destroy).pack(side=tk.RIGHT)

    def execute_rename(self):
        """执行重命名操作"""
        rename_plan = self.generate_rename_plan()
        if not rename_plan:
            return
        
        # 确认对话框
        input_dir = self.input_dir_var.get()
        output_dir = self.output_dir_var.get()
        
        if not messagebox.askyesno("确认操作", 
            f"即将重命名 {len(rename_plan)} 个文件\n\n"
            f"📁 从: {input_dir}\n"
            f"📁 到: {output_dir}\n\n"
            f"是否继续？"):
            return
        
        success_count = 0
        rename_table = []
        
        # 检查文件名冲突
        new_names = [new_name for _, new_name in rename_plan]
        if len(new_names) != len(set(new_names)):
            messagebox.showerror("错误", "生成的新文件名存在冲突，请调整命名格式！")
            return
        
        # 执行重命名
        for i, (old_name, new_name) in enumerate(rename_plan):
            old_path = os.path.join(input_dir, old_name)
            new_path = os.path.join(output_dir, new_name)
            
            # 如果输入输出文件夹相同，需要处理文件名冲突
            if input_dir == output_dir:
                counter = 1
                original_new_name = new_name
                while os.path.exists(new_path) and new_path != old_path:
                    name, ext = os.path.splitext(original_new_name)
                    new_name = f"{name}_{counter}{ext}"
                    new_path = os.path.join(output_dir, new_name)
                    counter += 1
            
            try:
                if old_path != new_path:
                    # 如果目标文件已存在，先删除（在不同文件夹的情况下）
                    if os.path.exists(new_path) and input_dir != output_dir:
                        os.remove(new_path)
                    
                    os.rename(old_path, new_path)
                    rename_table.append((i+1, old_name, new_name, "✅ 成功"))
                    success_count += 1
                else:
                    rename_table.append((i+1, old_name, new_name, "ℹ️ 无需更改"))
            except Exception as e:
                rename_table.append((i+1, old_name, new_name, f"❌ 错误: {str(e)}"))
        
        # 显示结果
        self.show_result_window(rename_table, success_count, len(rename_plan), input_dir)
        self.refresh_file_list()

    def show_result_window(self, rename_table, success_count, total_count, script_dir):
        """显示重命名结果窗口"""
        result_window = tk.Toplevel(self.root)
        result_window.title("重命名完成")
        result_window.geometry("800x500")
        result_window.transient(self.root)
        result_window.grab_set()
        
        # 居中显示
        result_window.update_idletasks()
        x = (result_window.winfo_screenwidth() // 2) - (800 // 2)
        y = (result_window.winfo_screenheight() // 2) - (500 // 2)
        result_window.geometry(f"+{x}+{y}")
        
        result_frame = ttk.Frame(result_window, padding="15")
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题和统计信息
        ttk.Label(result_frame, text="✅ 文件重命名完成", 
                 font=("微软雅黑", 16, "bold")).pack(pady=(0, 15))
        
        stats_frame = ttk.Frame(result_frame)
        stats_frame.pack(fill=tk.X, pady=(0, 15))
        
        success_rate = (success_count/total_count*100) if total_count > 0 else 0
        status_color = "#27ae60" if success_rate == 100 else "#e67e22" if success_rate > 0 else "#e74c3c"
        
        stats_text = f"成功处理: {success_count}/{total_count} 个文件  成功率: {success_rate:.1f}%"
        stats_label = ttk.Label(stats_frame, text=stats_text, font=("微软雅黑", 11, "bold"), 
                               foreground=status_color)
        stats_label.pack()
        
        # 重命名记录表格
        table_frame = ttk.LabelFrame(result_frame, text="重命名记录")
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建树形视图显示结果
        columns = ("序号", "原文件名", "新文件名", "状态")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        
        # 设置列标题
        for col in columns:
            tree.heading(col, text=col)
            if col == "序号":
                tree.column(col, width=50, anchor='center')
            elif col == "状态":
                tree.column(col, width=100, anchor='center')
            else:
                tree.column(col, width=200)
        
        # 添加数据
        for record in rename_table:
            tree.insert("", tk.END, values=record)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 按钮框架
        button_frame = ttk.Frame(result_frame)
        button_frame.pack(fill=tk.X, pady=(15, 0))
        
        ttk.Button(button_frame, text="✅ 完成", 
                  command=result_window.destroy).pack(side=tk.RIGHT)

def main():
    """主函数"""
    root = tk.Tk()
    app = ImprovedImageRenamer(root)
    root.mainloop()

if __name__ == "__main__":
    main()