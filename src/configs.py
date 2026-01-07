import json
import base64
from github import Github, GithubException


class GithubConfigManager:
    def __init__(self, token, repo_name):
        """
        :param token: GitHub Personal Access Token (PAT)
        :param repo_name: 格式为 "用户名/私有仓库名"
        """
        self.g = Github(token)
        self.repo = self.g.get_repo(repo_name)

    def read_json(self, file_path):
        """读取并解析 JSON 文件"""
        try:
            content = self.repo.get_contents(file_path)
            # 解码并转换为字典
            data = json.loads(content.decoded_content.decode("utf-8"))
            return data, content.sha
        except GithubException as e:
            print(f"读取失败: {e}")
            return None, None

    def write_json(self, file_path, data, message="Update config"):
        """写入或更新 JSON 文件"""
        # 将字典转换为美化的 JSON 字符串
        content_str = json.dumps(data, indent=4, ensure_ascii=False)

        try:
            # 尝试获取文件以获取 sha 值（更新必须）
            contents = self.repo.get_contents(file_path)
            self.repo.update_file(
                path=file_path,
                message=message,
                content=content_str,
                sha=contents.sha
            )
            print(f"成功更新 {file_path}")
        except GithubException:
            # 如果文件不存在，则创建新文件
            self.repo.create_file(
                path=file_path,
                message=message,
                content=content_str
            )
            print(f"成功创建 {file_path}")