import os
import json
import logging
from pathlib import Path

class DataManager:
    """
    数据管理模块，用于管理应用程序的数据路径和文件访问
    
    功能:
    - 加载数据路径 (.load(path))
    - 获取文件完整路径 (.file(filename))
    - 卸载数据路径 (.unload())
    - 自动创建必要目录
    - 配置文件管理
    
    使用示例:
        from data_manager import DataManager
        
        # 初始化数据管理器
        dm = DataManager()
        
        # 加载数据路径
        data_path = "C:/AppData/MyApp"
        dm.load(data_path)
        
        # 访问文件
        settings_file = dm.file("settings.json")
        print(f"配置文件路径: {settings_file}")
        
        # 访问子目录中的文件
        image_file = dm.file("images/logo.png")
        print(f"图片路径: {image_file}")
        
        # 卸载数据路径
        dm.unload()
    """
    
    def __init__(self, logger=None):
        """
        初始化数据管理器
        
        :param logger: 可选的日志记录器
        """
        self.data_path = None
        self.config = {}
        self.logger = logger or self._create_default_logger()

    def get_data(data):
        """获取应用程序数据路径"""
        return os.path.join(os.getenv('LOCALAPPDATA'), data)
    
    def _create_default_logger(self):
        """创建默认日志记录器"""
        logger = logging.getLogger('DataManager')
        logger.setLevel(logging.INFO)
        
        # 创建控制台处理器
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        # 创建格式化器
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        
        # 添加处理器
        logger.addHandler(ch)
        
        return logger
    
    def load(self, path):
        """
        加载数据路径
        
        :param path: 数据目录路径
        :return: True 如果加载成功，False 否则
        """
        try:
            # 确保路径是Path对象
            self.data_path = Path(path)
            
            # 确保数据目录存在
            self.data_path.mkdir(parents=True, exist_ok=True)
            
            # 加载配置文件
            self._load_config()
            
            return True
        except Exception as e:
            self.logger.error(f"加载数据路径失败: {e}")
            self.data_path = None
            return False
    
    def unload(self):
        """卸载数据路径"""
        self.logger.info(f"卸载数据路径: {self.data_path}")
        self.data_path = None
        self.config = {}
    
    def file(self, filename):
        """
        获取数据目录中文件的完整路径
        
        :param filename: 文件名或相对路径 (如 "settings.json" 或 "images/logo.png")
        :return: 文件的完整路径，如果数据路径未加载则返回 None
        """
        if not self.data_path:
            self.logger.warning("尝试访问文件，但数据路径未加载")
            return None
        
        # 创建完整文件路径
        file_path = self.data_path / filename
        
        # 确保目录存在
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        return file_path
    
    def _load_config(self):
        """加载配置文件"""
        config_file = self.file("settings.json")
        
        # 如果配置文件不存在，不创建默认配置
        if not config_file.exists():
            self.logger.info("配置文件不存在")
            self.config = {}  # 返回空配置
            return
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)

        except json.JSONDecodeError as e:
            self.logger.error(f"配置文件格式错误: {e}")
            # 使用空配置
            self.config = {}
        except Exception as e:
            self.logger.error(f"加载配置文件失败: {e}")
            self.config = {}
    
    def _save_config(self):
        """保存配置文件"""
        if not self.config:
            self.logger.warning("没有配置可保存")
            return False
        
        config_file = self.file("settings.json")
        
        try:
            # 直接保存文件，不创建备份
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            self.logger.error(f"保存配置文件失败: {e}")
            return False
    
    def _get_default_config(self):
        """获取主程序所需的默认配置 - 返回空配置"""
        return {}
    
    def get_config(self, key, default=None):
        """
        获取配置项
        
        :param key: 配置键名
        :param default: 如果键不存在时的默认值
        :return: 配置值
        """
        return self.config.get(key, default)
    
    def set_config(self, key, value):
        """
        设置配置项
        
        :param key: 配置键名
        :param value: 配置值
        """
        self.config[key] = value
        self._save_config()
    
    def is_loaded(self):
        """检查数据路径是否已加载"""
        return self.data_path is not None
    
    def loadjson(self, filename, default=None):
        """
        加载并解析JSON文件内容
        
        :param filename: JSON文件名或相对路径
        :param default: 如果文件不存在或解析失败时返回的默认值
        :return: 解析后的JSON数据（字典或列表），或默认值
        """
        if not self.is_loaded():
            self.logger.warning("尝试加载JSON文件，但数据路径未加载")
            return default
        
        file_path = self.file(filename)
        
        # 检查文件是否存在
        if not file_path.exists():
            self.logger.info(f"JSON文件不存在: {file_path}")
            return default
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON文件格式错误: {file_path} - {e}")
            return default
        except Exception as e:
            self.logger.error(f"加载JSON文件失败: {file_path} - {e}")
            return default
    
    def savejson(self, filename, data):
        """
        保存数据到JSON文件
        
        :param filename: JSON文件名或相对路径
        :param data: 要保存的数据（字典或列表）
        :return: True 如果保存成功，False 否则
        """
        if not self.is_loaded():
            self.logger.warning("尝试保存JSON文件，但数据路径未加载")
            return False
        
        file_path = self.file(filename)
        
        try:
            # 确保目录存在
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                # 使用自定义顺序序列化 JSON
                ordered_data = {
                    "Version": data.get("Version", 1.0),
                    "Initialization": data.get("Initialization", False),
                    "Language": data.get("Language", "English"),
                    "GamePath": data.get("GamePath", ""),
                    "LastDate": data.get("LastDate", ""),
                    "Time": data.get("Time", 0)
                }
                json.dump(ordered_data, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            self.logger.error(f"保存JSON文件失败: {file_path} - {e}")
            return False