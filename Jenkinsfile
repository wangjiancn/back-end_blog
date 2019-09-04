pipeline {
    agent none
    environment {
        CI = 'true'
    }
    stages {
        stage('Build') {
            agent any
            steps{
                script{
                    def date = new Date().format("YYYYMMdd")    // 获取一个 20190101 格式的时间字符串
                    def commit = env.GIT_COMMIT
                    def short_commit = commit ? commit[0..6] : "" // 取前6为git sha
                    def local_tag = date + "-" + short_commit   // 20190101-d234k4
                    def IMAGE_NAME = "${env.DOCKER_REG_ALI}/blog-backend"
                    docker.withRegistry("https://${env.DOCKER_REG_ALI}", "docker") {
                        image = docker.build("${IMAGE_NAME}:${local_tag}")
                    }
                    //do some test
                    sh "docker rmi ${IMAGE_NAME}:${local_tag}"  //删除本地镜像
                }
            }
        }
        stage('Push') {
            agent any
            when { tag "*" }    // 如果有tag推送镜像,没有则跳过
            steps {
                script{
                    def date = new Date().format("YYYYMMdd")
                    def commit = env.GIT_COMMIT
                    def short_commit = commit ? commit[0..6] : "" 
                    def local_tag = date + "-" + short_commit   
                    IMAGE_NAME = "${env.DOCKER_REG_ALI}/blog-backend"
                    // 多个标签取最后一个
                    tag = sh(returnStdout: true, script: "git tag -l --points-at HEAD").trim().split("\n")[-1]
                    major = tag.split('\\.')[0]
                    if(tag){
                        docker.withRegistry("https://${env.DOCKER_REG_ALI}", "docker") {
                            image = docker.build(
                                "${IMAGE_NAME}:${tag}",
                                "--build-arg version=${tag} --build-arg date=${local_tag} ."
                                )   // version: 1.1.1
                            image.push(major)   // majon version: 1
                            image.push("latest")    // latest version
                        }
                    }
                }
                sh "docker rmi ${IMAGE_NAME}:${major}" 
                sh "docker rmi ${IMAGE_NAME}:${tag}" // 本地只保留最新版本
                sh "echo Deploy completed"
            }
        }
    }
}