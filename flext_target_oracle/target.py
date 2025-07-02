"""Oracle target implementation."""

import sys
import json
import logging
from typing import Dict, Any, Optional
import singer
import cx_Oracle


class TargetOracle:
    """Singer target for Oracle database."""
    
    def __init__(self, config: Dict[str, Any], state: Optional[Dict[str, Any]] = None):
        """Initialize Oracle target.
        
        Args:
            config: Target configuration
            state: Current state
        """
        self.config = config
        self.state = state or {}
        self.connection = None
        self.logger = logging.getLogger(__name__)
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        
    def connect(self):
        """Connect to Oracle database."""
        try:
            dsn = cx_Oracle.makedsn(
                self.config['host'],
                self.config['port'],
                service_name=self.config['database']
            )
            
            self.connection = cx_Oracle.connect(
                user=self.config['user'],
                password=self.config['password'],
                dsn=dsn
            )
            
            self.logger.info("Connected to Oracle database")
            
        except Exception as e:
            self.logger.error(f"Failed to connect to Oracle: {e}")
            raise
    
    def listen(self):
        """Listen for Singer messages on stdin."""
        if not self.connection:
            self.connect()
            
        for line in sys.stdin:
            try:
                message = singer.parse_message(line)
                self.handle_message(message)
            except Exception as e:
                self.logger.error(f"Error processing message: {e}")
                continue
    
    def handle_message(self, message):
        """Handle a Singer message.
        
        Args:
            message: Parsed Singer message
        """
        if isinstance(message, singer.RecordMessage):
            self.handle_record(message)
        elif isinstance(message, singer.SchemaMessage):
            self.handle_schema(message)
        elif isinstance(message, singer.StateMessage):
            self.handle_state(message)
    
    def handle_record(self, message):
        """Handle a record message.
        
        Args:
            message: Record message
        """
        self.logger.info(f"Processing record for stream: {message.stream}")
        # TODO: Implement record insertion logic
        
    def handle_schema(self, message):
        """Handle a schema message.
        
        Args:
            message: Schema message
        """
        self.logger.info(f"Processing schema for stream: {message.stream}")
        # TODO: Implement schema creation/update logic
        
    def handle_state(self, message):
        """Handle a state message.
        
        Args:
            message: State message
        """
        self.state = message.value
        singer.write_state(self.state)