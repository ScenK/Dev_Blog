
##  同项目文件 bitbucket 分支请见: <https://bitbucket.org/Scen/dev_blog/> 为Dev开发版本
##  使用Dev版本 会有不同程度的不稳定性 使用时请注意 
##
### Copyright 2012-2013 Dev-engine
###
### Dev-Blog Python-Release Based On Tornado and MongoDB
###
### <http://tuzii.me/>
###
### License for the specific language governing permissions and limitations
### under the License.
###
### Author : Scen.Kang

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

 文件目录结构:

    Dev-Blog/
        app/
        |---application.py                 整个应用的Settings
            runserver.py                   用来启动web服务器
            urls.py                        route相关
            yuicompressor.jar              YUI文件压缩器
        |--- Config/                       相关配置文件
        |--- Handler/                      MVC中 C 结构
        |--- Model/                        MVC中 M 结构
        |--- Views/                        MVC中 V 结构
            |--- Admin/                    后端Admin页面
            |--- Diary/                    日志组建
            |--- modules/                  复用前端组建
        |--- static/                       webroot目录 保存js css images等文件
            |--- css/
            |--- less/
            |--- js/
            |--- lib/
            |--- img/
            |--- uploads/
            favicon.ico
            robots.txt
        |--- lib/                           集成脚本
            |--- kid.py                     MongoDB自增ObjectId生成器
            |--- email_util.py              SMTP邮件发送器
        |--- fabfile/                       集成发布Fabric命令
        lib/
        README.md
        requirements.txt                    Python基础安装包列表

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
+ 安装须知:

    * 项目Wiki地址: <https://github.com/ScenK/dev_blog/wiki/>
    * 博客地址: <http://tuzii.me/>
    * 推荐使用独立VPS
        本博客线上环境: Amazon EC2 + Ubuntu12.04 + Python2.7.3 + Nginx + Tornado + MongoDB2.0.2
    * 基础环境:
        Linux + Tornado + Python + MongoDB
    * 可选环境:
        前端使用nginx做多线程反向代理
    * 基础环境配好后按照requirements.txt里列出的相关软件包装好
        推荐使用pip批量安装
    * 启动相关进程(MongoDB, Nginx或裸跑Tornado)
    * 进入dev-blog/app/
        - 编辑 Config/config.py.sample 更改网站相关设置
        - 执行fab build 进行初始化部属
        - 执行fab deploy 进行less编译和css js 压缩(需要安装lessc编译环境)
        - 执行fab test 开启服务器进程(或者在Supervisor开启python多进程)
        - 每次改动的代码更新都可以使用fab update 进行服务端代码自动更新


+ 待完成:

    * 后端管理功能逐项添加
    * api 的整理添加


+ 开发&使用须知:

    * 此博客所有代码均开源 这个想法起源于我刚接触Python的时候 并没有好的、完整的项目来接触 也不知Tornado MongoDB Fabric 等如何融合在一起使用 于是下决心搞定后开源掉 给同样困惑的人以帮助和参考
    * 欢迎各路GEEK来join我的team: Dev-engine 当然希望你是一把好手 对代码有洁癖 对程序有要求的人
    * 欢迎觉得界面很丑 希望帮助我来改进前端体验的设计师朋友的加入
    * 欢迎各种folk 各种提pull request 和issue 我会积极的去解决和改进
    * 最后 本人是12年刚刚毕业的学生 而且并不是计算机出身 所以半路出家难免会犯一些低级错误 希望各位不吝赐教

###### Do it yourself and make joy :)
