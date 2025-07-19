import os
import json

class ConfigManager:
    CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".fast_note_config.json")
    
    def __init__(self):
        self.config = {}
    
    def load_config(self):
        """加载配置文件"""
        if os.path.exists(self.CONFIG_PATH):
            try:
                with open(self.CONFIG_PATH, "r") as config_file:
                    self.config = json.load(config_file)
            except Exception:
                self.config = {}
    
    def save_config(self):
        """保存配置文件"""
        try:
            with open(self.CONFIG_PATH, "w") as config_file:
                json.dump(self.config, config_file)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get(self, key, default=None):
        """获取配置值"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """设置配置值"""
        self.config[key] = value