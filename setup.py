from setuptools import setup

setup(
    name='hachinai_scraping',
    version='0.01',
    packages=['hachinai_scraping'],
    url='https://github.com/kibehiro/hachinai-charadata-scraping',
    license='MIT',
    author='KIBE',
    description='ハチナイのキャラデータをatwikiからスクレイピングしてDBに格納します',
    install_requires=['psycopg2', 'requests', 'beautifulsoup4', 'jsonschema', 'python-dotenv']
)
