# OpenTutor :D

📦 一个基于LLM的人工智能学习助手的beta版，功能聚焦于根据各种课程材料，笔记，作业，往年考试题目及例题模拟出考试题目，为教学人员提供帮助！(或者预测你的期末考试题目？）

前端使用 [Vue](https://github.com/vuejs/vue)，后端使用微框架 [Flask](https://github.com/pallets/flask)。

## 使用方法



## 项目结构

```
├── front # 前端
│    ├── package.json # 前端依赖
│    ├── package-lock.json
│    ├── public
│    ├── src
│    │    ├── App.vue # 主页面
│    │    ├── components # 子组件
│    │	  │		├── CreateCourse.vue
│    │	  │		├── Results.vue
│    │	  │		├── UploadMaterial.vue
│    │	  │		├── Waiting.vue
│    │	  │		├── Welcome.vue
│    │	  │		├── Handle.vue # 链接3个主要功能
│    │    ├── assets # 静态资源
│    │    └── main.js
│    └── vite.config.js
├── fastAPI # 后端
│    ├── main.py
│    └── requirements.txt # 后端依赖
├── README.md
├── LICENSE
└── .gitignore
```

## 许可


## 参考

celery 不支持 windows 

请在测试/开发环境中使用 Gevent (Windows)，或将线程数限制为1.
```angular2html
pip install gevent

celery -A celery_worker worker -l info -P gevent
```

- [Vite 官方中文文档](https://cn.vitejs.dev/guide/why.html)
- [Flask 官方文档](https://flask.palletsprojects.com/en/1.1.x/)
