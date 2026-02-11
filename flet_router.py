import flet as ft
from typing import Dict,Type

class Router:
    def __init__(self):
        self.routes : Dict[str, ft.View] = {}

    def route(self, path:str):
        """
        返回一个类装饰器，用于注册路由
        """
        def decorator(cls):
            if not issubclass(cls, ft.View):
                raise TypeError(f"类 {cls.__name__} 必须继承自 flet.View")
            self.routes[path] = cls(route=path)
            return cls
        return decorator

    def navigate(self, path, **kwargs):
        """
        导航到指定路由
        """
        if path not in self.routes:
            raise ValueError(f"路由 {path} 不存在")
        return self.routes[path]


router = Router()