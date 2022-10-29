. /jenkins/workspace/venv/bin/activate

export PORT=PORT_PLACEHOLDER
export ENVIRONMENT=ENV_TYPE_PLACEHOLDER

cd /opt/tnik
python install.py
python server.py