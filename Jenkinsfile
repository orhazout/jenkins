@Library('EZJEL') _

def dockerImage
pipeline {
    agent {
        kubernetes {
        label 'pets-app'
        idleMinutes 5
        yamlFile 'build-pod.yaml'
        defaultContainer 'pets-app-docker-helm-build'
        }
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '5'))
    }

    environment {
        DOCKER_IMAGE = 'orhazout/pets-app'
        HELM_PACKAGE = 'orhazout/pets-app-chart'
        NAME_PACKEGE = 'pets-app-chart'
    }

    stages {
        stage('Setup') {
            steps {
                checkout scm
                script {
                    ezEnvSetup.initEnv()
                    def id = ezUtils.getUniqueBuildIdentifier()
                    if(BRANCH_NAME == 'main')
                    {
                        env.BUILD_ID = "1."+id
                    }
                    else {
                        env.BUILD_ID = "0." + id
                    }
                    currentBuild.displayName+=" {build-name:"+env.BUILD_ID+"}"
                }
            }
        }

        stage('Build Docker image') {
            steps {
                script {
                    dockerImage = docker.build(DOCKER_IMAGE+":"+env.BUILD_ID,"--no-cache .")
                }
            }
        }

        stage('Build Helm Chart') {
            steps {
                sh 'helm lint ${NAME_PACKEGE}'
                sh 'helm package ${NAME_PACKEGE} --version '+env.BUILD_ID
            }
        }


        
        stage('Push Docker image') {
            // when {
            //     branch 'main'
            // }
            steps {
                script {
                    docker.withRegistry("https://registry.hub.docker.com", 'orhazout') {
                        dockerImage.push()
                    }
                }
            }
        }

        stage('Push HELM chart') {
            // when {
            //     branch 'main'
            // }
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'orhazout', passwordVariable: 'DOCKERHUB_PASSWORD', usernameVariable: 'DOCKERHUB_USER')]) {
                        sh "docker login -u ${DOCKERHUB_USER} -p ${DOCKERHUB_PASSWORD}"
                        sh "helm push ${NAME_PACKEGE}-"+env.BUILD_ID+".tgz oci://registry-1.docker.io/orhazout"
                    }
                }
            }
        }
    }
}
