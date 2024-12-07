# Hadoop settings
HADOOP_NAMENODE = 'localhost:9000'
HDFS_URL = f'http://{HADOOP_NAMENODE}'

# Add the Hadoop home directory
HADOOP_HOME = 'C:\\hadoop'

# WebHDFS settings
WEBHDFS_URL = 'http://localhost:9870/webhdfs/v1'

# Hadoop configuration
HADOOP_CONF = {
    'runners': {
        'hadoop': {
            'hadoop_home': HADOOP_HOME,
            'hadoop_streaming_jar': f'{HADOOP_HOME}\\share\\hadoop\\tools\\lib\\hadoop-streaming-3.2.4.jar',
            'jobconf': {
                'mapreduce.job.reduces': 1,
                'mapreduce.map.memory.mb': 1024,
                'mapreduce.reduce.memory.mb': 1024,
            },
            'hdfs_url': HDFS_URL,
            'hadoop_extra_args': [
                '-D',
                f'fs.defaultFS=hdfs://{HADOOP_NAMENODE}'
            ],
            'python_bin': 'python',
            'setup': [
                f'set PYTHONPATH=%PYTHONPATH%;C:\\Users\\LENOVO\\CLOUDEXAM\\eKigega'
            ],
            'local_tmp_dir': 'C:\\Users\\LENOVO\\CLOUDEXAM\\eKigega\\tmp',
            'upload_files': [
                'inventory/mapreduce_jobs.py'
            ]
        }
    }
}