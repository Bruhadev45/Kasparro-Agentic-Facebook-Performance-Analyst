"""Logger utility for structured logging."""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any


class Logger:
    """Structured JSON logger for agent execution traces."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize logger.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.logs_dir = Path(config['outputs']['logs_dir'])
        self.logs_dir.mkdir(exist_ok=True)
        
        self.session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.log_file = self.logs_dir / f'execution_{self.session_id}.json'
        self.logs = []
    
    def log(self, agent: str, event: str, data: Dict[str, Any]):
        """Log an event.
        
        Args:
            agent: Agent name
            event: Event type
            data: Event data
        """
        log_entry = {
            'timestamp': self.get_timestamp(),
            'agent': agent,
            'event': event,
            'data': data
        }
        
        self.logs.append(log_entry)
        
        # Write to file
        with open(self.log_file, 'w') as f:
            json.dump(self.logs, f, indent=2)
        
        # Also print to console if INFO level
        if self.config['logging']['level'] == 'INFO':
            print(f"[{log_entry['timestamp']}] {agent}.{event}: {json.dumps(data)}")
    
    def get_timestamp(self) -> str:
        """Get current timestamp.
        
        Returns:
            ISO format timestamp
        """
        return datetime.now().isoformat()
    
    def get_logs(self) -> list:
        """Get all logs.
        
        Returns:
            List of log entries
        """
        return self.logs
