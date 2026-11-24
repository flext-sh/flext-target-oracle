# Docs Audit Report

Scope: flext-target-oracle
Files scanned: 40
Issues: 20

| file | type | severity | message |
| --- | --- | --- | --- |
| docs/TODO.md | python_codeblock | medium | block #0: blank-lines-top-level: Expected 2 blank lines, found 0
  --> docs/TODO.md#block0.py:11:1
   |
 9 |     Sequence,
10 | )
11 | class FlextOracleTarget(Target):
   | ^^^^^
12 |     def _test_connection(self) -> bool:
13 |         return self._test_connection_impl()
   |
help: Add missing blank line(s)

invalid-syntax: Expected an indented block after function definition
  --> docs/TODO.md#block0.py:15:53
   |
13 |         return self._test_connection_impl()
14 |
15 |     def _write_record(self, record: Record) -> None:
   |                                                     ^
16 |         # Implementar método Singer padrão
   |

no-indented-block: Expected an indented block
  --> docs/TODO.md#block0.py:16:44
   |
15 |     def _write_record(self, record: Record) -> None:
16 |         # Implementar método Singer padrão
   |                                           ^

Found 3 errors. |
| docs/TODO.md | python_codeblock | medium | block #1: invalid-syntax: Expected `)`, found `...`
 --> docs/TODO.md#block1.py:1:25
  |
1 | def ensure_table_exists(...)  # Não precisa ser
  |                         ^^^
2 | def _create_table(...)        # Não precisa ser
  |

invalid-syntax: Expected newline, found `)`
 --> docs/TODO.md#block1.py:1:28
  |
1 | def ensure_table_exists(...)  # Não precisa ser
  |                            ^
2 | def _create_table(...)        # Não precisa ser
  |

invalid-syntax: Expected a statement
 --> docs/TODO.md#block1.py:1:48
  |
1 | def ensure_table_exists(...)  # Não precisa ser
  |                                                ^
2 | def _create_table(...)        # Não precisa ser
  |

invalid-syntax: Expected `)`, found `...`
 --> docs/TODO.md#block1.py:2:19
  |
1 | def ensure_table_exists(...)  # Não precisa ser
2 | def _create_table(...)        # Não precisa ser
  |                   ^^^

invalid-syntax: Expected newline, found `)`
 --> docs/TODO.md#block1.py:2:22
  |
1 | def ensure_table_exists(...)  # Não precisa ser
2 | def _create_table(...)        # Não precisa ser
  |                      ^

invalid-syntax: Expected a statement
 --> docs/TODO.md#block1.py:2:48
  |
1 | def ensure_table_exists(...)  # Não precisa ser
2 | def _create_table(...)        # Não precisa ser
  |                                                ^

Found 6 errors. |
| docs/TODO.md | python_codeblock | medium | block #2: blank-lines-top-level: Expected 2 blank lines, found 0
  --> docs/TODO.md#block2.py:11:1
   |
 9 |     Sequence,
10 | )
11 | def _evolve_table_schema(self, table_name: str, new_schema: dict):
   | ^^^
12 |     # Implementar ALTER TABLE baseado em diff de schema
   |
help: Add missing blank line(s)

invalid-syntax: Expected an indented block after function definition
  --> docs/TODO.md#block2.py:11:67
   |
 9 |     Sequence,
10 | )
11 | def _evolve_table_schema(self, table_name: str, new_schema: dict):
   |                                                                   ^
12 |     # Implementar ALTER TABLE baseado em diff de schema
   |

Found 2 errors. |
| docs/TODO.md | python_codeblock | medium | block #3: blank-lines-top-level: Expected 2 blank lines, found 0
  --> docs/TODO.md#block3.py:11:1
   |
 9 |     Sequence,
10 | )
11 | class OracleConnectionFactory:
   | ^^^^^
12 |     @staticmethod
13 |     def create_api(settings: FlextOracleTargetSettings) -> FlextDbOracleApi:
   |
help: Add missing blank line(s)

invalid-syntax: Expected an indented block after function definition
  --> docs/TODO.md#block3.py:13:77
   |
11 | class OracleConnectionFactory:
12 |     @staticmethod
13 |     def create_api(settings: FlextOracleTargetSettings) -> FlextDbOracleApi:
   |                                                                             ^
14 |         # Factory para criação de conexões
   |

no-indented-block: Expected an indented block
  --> docs/TODO.md#block3.py:14:44
   |
13 |     def create_api(settings: FlextOracleTargetSettings) -> FlextDbOracleApi:
14 |         # Factory para criação de conexões
   |                                           ^

Found 3 errors. |
| docs/TODO.md | python_codeblock | medium | block #4: blank-lines-top-level: Expected 2 blank lines, found 0
  --> docs/TODO.md#block4.py:11:1
   |
 9 |     Sequence,
10 | )
11 | @pytest.fixture
   | ^
12 | def oracle_connection():
13 |     # Fixture para conexão Oracle real em testes de integração
   |
help: Add missing blank line(s)

invalid-syntax: Expected an indented block after function definition
  --> docs/TODO.md#block4.py:15:1
   |
13 |     # Fixture para conexão Oracle real em testes de integração
14 |
15 | @pytest.fixture
   | ^
16 | def malicious_data():
17 |     # Fixture para testar SQL injection
   |

no-indented-block: Expected an indented block
  --> docs/TODO.md#block4.py:15:1
   |
13 |     # Fixture para conexão Oracle real em testes de integração
14 |
15 | @pytest.fixture
   | ^
16 | def malicious_data():
17 |     # Fixture para testar SQL injection
   |

invalid-syntax: Expected an indented block after function definition
  --> docs/TODO.md#block4.py:16:22
   |
15 | @pytest.fixture
16 | def malicious_data():
   |                      ^
17 |     # Fixture para testar SQL injection
   |

Found 4 errors. |
| docs/development.md | python_codeblock | medium | block #0: invalid-syntax: Got unexpected token `
  --> docs/development.md#block0.py:47:9
   |
45 |     def __init__(self, field):
46 |         self.field = field  # No validation!
47 |         ```
   |         ^
48 | ## FLEXT Pattern Implementation
   |

invalid-syntax: Got unexpected token `
  --> docs/development.md#block0.py:47:10
   |
45 |     def __init__(self, field):
46 |         self.field = field  # No validation!
47 |         ```
   |          ^
48 | ## FLEXT Pattern Implementation
   |

invalid-syntax: Got unexpected token `
  --> docs/development.md#block0.py:47:11
   |
45 |     def __init__(self, field):
46 |         self.field = field  # No validation!
47 |         ```
   |           ^
48 | ## FLEXT Pattern Implementation
   |

invalid-syntax: Expected a statement
  --> docs/development.md#block0.py:47:12
   |
45 |     def __init__(self, field):
46 |         self.field = field  # No validation!
47 |         ```
   |            ^
48 | ## FLEXT Pattern Implementation
   |

multiple-leading-hashes-for-block-comment: Too many leading `#` before block comment
  --> docs/development.md#block0.py:48:1
   |
46 |         self.field = field  # No validation!
47 |         ```
48 | ## FLEXT Pattern Implementation
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
49 |
50 | ### r Railway Pattern
   |
help: Remove leading `#`

multiple-leading-hashes-for-block-comment: Too many leading `#` before block comment
  --> docs/development.md#block0.py:50:1
   |
48 | ## FLEXT Pattern Implementation
49 |
50 | ### r Railway Pattern
   | ^^^^^^^^^^^^^^^^^^^^^
51 |
52 | ```text
   |
help: Remove leading `#`

blank-lines-after-function-or-class: Expected 2 blank lines after class or function definition, found (1)
  --> docs/development.md#block0.py:52:1
   |
50 | ### r Railway Pattern
51 |
52 | ```text
   | ^
53 | from __future__ import annotations
   |
help: Add missing blank line(s)

invalid-syntax: Got unexpected token `
  --> docs/development.md#block0.py:52:1
   |
50 | ### r Railway Pattern
51 |
52 | ```text
   | ^
53 | from __future__ import annotations
   |

invalid-syntax: Got unexpected token `
  --> docs/development.md#block0.py:52:2
   |
50 | ### r Railway Pattern
51 |
52 | ```text
   |  ^
53 | from __future__ import annotations
   |

invalid-syntax: Got unexpected token `
  --> docs/development.md#block0.py:52:3
   |
50 | ### r Railway Pattern
51 |
52 | ```text
   |   ^
53 | from __future__ import annotations
   |

invalid-syntax: Got unexpected token `
  --> docs/development.md#block0.py:89:1
   |
88 |     return r[bool].ok(value=True)
89 | ```
   | ^
90 | ### Configuration Patterns
   |

blank-lines-after-function-or-class: Expected 2 blank lines after class or function definition, found (0)
  --> docs/development.md#block0.py:89:1
   |
88 |     return r[bool].ok(value=True)
89 | ```
   | ^
90 | ### Configuration Patterns
   |
help: Add missing blank line(s)

invalid-syntax: Got unexpected token `
  --> docs/development.md#block0.py:89:2
   |
88 |     return r[bool].ok(value=True)
89 | ```
   |  ^
90 | ### Configuration Patterns
   |

invalid-syntax: Got unexpected token `
  --> docs/development.md#block0.py:89:3
   |
88 |     return r[bool].ok(value=True)
89 | ```
   |   ^
90 | ### Configuration Patterns
   |

invalid-syntax: Expected a statement
  --> docs/development.md#block0.py:89:4
   |
88 |     return r[bool].ok(value=True)
89 | ```
   |    ^
90 | ### Configuration Patterns
   |

multiple-leading-hashes-for-block-comment: Too many leading `#` before block comment
  --> docs/development.md#block0.py:90:1
   |
88 |     return r[bool].ok(value=True)
89 | ```
90 | ### Configuration Patterns
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^
91 |
92 | ```text
   |
help: Remove leading `#`

invalid-syntax: Got unexpected token `
  --> docs/development.md#block0.py:92:1
   |
90 | ### Configuration Patterns
91 |
92 | ```text
   | ^
93 | from __future__ import annotations
   |

invalid-syntax: Got unexpected token `
  --> docs/development.md#block0.py:92:2
   |
90 | ### Configuration Patterns
91 |
92 | ```text
   |  ^
93 | from __future__ import annotations
   |

invalid-syntax: Got unexpected token `
  --> docs/development.md#block0.py:92:3
   |
90 | ### Configuration Patterns
91 |
92 | ```text
   |   ^
93 | from __future__ import annotations
   |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:128:1
    |
126 |         validator = ConfigurationValidator()
127 |         return validator.validate(self)
128 | ```
    | ^
129 | ### Logging Patterns
    |

blank-lines-after-function-or-class: Expected 2 blank lines after class or function definition, found (0)
   --> docs/development.md#block0.py:128:1
    |
126 |         validator = ConfigurationValidator()
127 |         return validator.validate(self)
128 | ```
    | ^
129 | ### Logging Patterns
    |
help: Add missing blank line(s)

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:128:2
    |
126 |         validator = ConfigurationValidator()
127 |         return validator.validate(self)
128 | ```
    |  ^
129 | ### Logging Patterns
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:128:3
    |
126 |         validator = ConfigurationValidator()
127 |         return validator.validate(self)
128 | ```
    |   ^
129 | ### Logging Patterns
    |

invalid-syntax: Expected a statement
   --> docs/development.md#block0.py:128:4
    |
126 |         validator = ConfigurationValidator()
127 |         return validator.validate(self)
128 | ```
    |    ^
129 | ### Logging Patterns
    |

multiple-leading-hashes-for-block-comment: Too many leading `#` before block comment
   --> docs/development.md#block0.py:129:1
    |
127 |         return validator.validate(self)
128 | ```
129 | ### Logging Patterns
    | ^^^^^^^^^^^^^^^^^^^^
130 |
131 | ```text
    |
help: Remove leading `#`

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:131:1
    |
129 | ### Logging Patterns
130 |
131 | ```text
    | ^
132 | from __future__ import annotations
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:131:2
    |
129 | ### Logging Patterns
130 |
131 | ```text
    |  ^
132 | from __future__ import annotations
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:131:3
    |
129 | ### Logging Patterns
130 |
131 | ```text
    |   ^
132 | from __future__ import annotations
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:179:1
    |
177 |         )
178 |         raise
179 | ```
    | ^
180 | ## Oracle Integration Development
    |

blank-lines-after-function-or-class: Expected 2 blank lines after class or function definition, found (0)
   --> docs/development.md#block0.py:179:1
    |
177 |         )
178 |         raise
179 | ```
    | ^
180 | ## Oracle Integration Development
    |
help: Add missing blank line(s)

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:179:2
    |
177 |         )
178 |         raise
179 | ```
    |  ^
180 | ## Oracle Integration Development
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:179:3
    |
177 |         )
178 |         raise
179 | ```
    |   ^
180 | ## Oracle Integration Development
    |

invalid-syntax: Expected a statement
   --> docs/development.md#block0.py:179:4
    |
177 |         )
178 |         raise
179 | ```
    |    ^
180 | ## Oracle Integration Development
    |

multiple-leading-hashes-for-block-comment: Too many leading `#` before block comment
   --> docs/development.md#block0.py:180:1
    |
178 |         raise
179 | ```
180 | ## Oracle Integration Development
    | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
181 |
182 | ### Database Connection Testing
    |
help: Remove leading `#`

multiple-leading-hashes-for-block-comment: Too many leading `#` before block comment
   --> docs/development.md#block0.py:182:1
    |
180 | ## Oracle Integration Development
181 |
182 | ### Database Connection Testing
    | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
183 |
184 | ```text
    |
help: Remove leading `#`

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:184:1
    |
182 | ### Database Connection Testing
183 |
184 | ```text
    | ^
185 | # Test Oracle connectivity manually
186 | from flext_core import u
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:184:2
    |
182 | ### Database Connection Testing
183 |
184 | ```text
    |  ^
185 | # Test Oracle connectivity manually
186 | from flext_core import u
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:184:3
    |
182 | ### Database Connection Testing
183 |
184 | ```text
    |   ^
185 | # Test Oracle connectivity manually
186 | from flext_core import u
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:198:1
    |
196 | else:
197 |     u.Cli.print(f"Connection failed: {result.error}")
198 | ```
    | ^
199 | ### Table Management Development
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:198:2
    |
196 | else:
197 |     u.Cli.print(f"Connection failed: {result.error}")
198 | ```
    |  ^
199 | ### Table Management Development
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:198:3
    |
196 | else:
197 |     u.Cli.print(f"Connection failed: {result.error}")
198 | ```
    |   ^
199 | ### Table Management Development
    |

invalid-syntax: Expected a statement
   --> docs/development.md#block0.py:198:4
    |
196 | else:
197 |     u.Cli.print(f"Connection failed: {result.error}")
198 | ```
    |    ^
199 | ### Table Management Development
    |

multiple-leading-hashes-for-block-comment: Too many leading `#` before block comment
   --> docs/development.md#block0.py:199:1
    |
197 |     u.Cli.print(f"Connection failed: {result.error}")
198 | ```
199 | ### Table Management Development
    | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
200 |
201 | ```text
    |
help: Remove leading `#`

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:201:1
    |
199 | ### Table Management Development
200 |
201 | ```text
    | ^
202 | from __future__ import annotations
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:201:2
    |
199 | ### Table Management Development
200 |
201 | ```text
    |  ^
202 | from __future__ import annotations
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:201:3
    |
199 | ### Table Management Development
200 |
201 | ```text
    |   ^
202 | from __future__ import annotations
    |

blank-lines-after-function-or-class: Expected 2 blank lines after class or function definition, found (0)
   --> docs/development.md#block0.py:237:1
    |
235 |     else:
236 |         u.Cli.print(f"Record loading failed: {result.error}")
237 | ```
    | ^
238 | ## Debugging and Troubleshooting
    |
help: Add missing blank line(s)

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:237:1
    |
235 |     else:
236 |         u.Cli.print(f"Record loading failed: {result.error}")
237 | ```
    | ^
238 | ## Debugging and Troubleshooting
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:237:2
    |
235 |     else:
236 |         u.Cli.print(f"Record loading failed: {result.error}")
237 | ```
    |  ^
238 | ## Debugging and Troubleshooting
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:237:3
    |
235 |     else:
236 |         u.Cli.print(f"Record loading failed: {result.error}")
237 | ```
    |   ^
238 | ## Debugging and Troubleshooting
    |

invalid-syntax: Expected a statement
   --> docs/development.md#block0.py:237:4
    |
235 |     else:
236 |         u.Cli.print(f"Record loading failed: {result.error}")
237 | ```
    |    ^
238 | ## Debugging and Troubleshooting
    |

multiple-leading-hashes-for-block-comment: Too many leading `#` before block comment
   --> docs/development.md#block0.py:238:1
    |
236 |         u.Cli.print(f"Record loading failed: {result.error}")
237 | ```
238 | ## Debugging and Troubleshooting
    | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
239 |
240 | ### Common Development Issues
    |
help: Remove leading `#`

multiple-leading-hashes-for-block-comment: Too many leading `#` before block comment
   --> docs/development.md#block0.py:240:1
    |
238 | ## Debugging and Troubleshooting
239 |
240 | ### Common Development Issues
    | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
241 |
242 | #### 1. Oracle Connection Issues
    |
help: Remove leading `#`

multiple-leading-hashes-for-block-comment: Too many leading `#` before block comment
   --> docs/development.md#block0.py:242:1
    |
240 | ### Common Development Issues
241 |
242 | #### 1. Oracle Connection Issues
    | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
243 |
244 | ```bash
    |
help: Remove leading `#`

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:244:1
    |
242 | #### 1. Oracle Connection Issues
243 |
244 | ```bash
    | ^
245 | # Check Oracle container status
246 | docker ps -a --filter oracle
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:244:2
    |
242 | #### 1. Oracle Connection Issues
243 |
244 | ```bash
    |  ^
245 | # Check Oracle container status
246 | docker ps -a --filter oracle
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:244:3
    |
242 | #### 1. Oracle Connection Issues
243 |
244 | ```bash
    |   ^
245 | # Check Oracle container status
246 | docker ps -a --filter oracle
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:246:8
    |
244 | ```bash
245 | # Check Oracle container status
246 | docker ps -a --filter oracle
    |        ^^
247 | docker logs oracle-test
    |

missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
   --> docs/development.md#block0.py:246:11
    |
244 | ```bash
245 | # Check Oracle container status
246 | docker ps -a --filter oracle
    |           ^
247 | docker logs oracle-test
    |
help: Add missing whitespace

missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
   --> docs/development.md#block0.py:246:14
    |
244 | ```bash
245 | # Check Oracle container status
246 | docker ps -a --filter oracle
    |              ^
247 | docker logs oracle-test
    |
help: Add missing whitespace

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:246:23
    |
244 | ```bash
245 | # Check Oracle container status
246 | docker ps -a --filter oracle
    |                       ^^^^^^
247 | docker logs oracle-test
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:247:8
    |
245 | # Check Oracle container status
246 | docker ps -a --filter oracle
247 | docker logs oracle-test
    |        ^^^^
248 |
249 | # Debug with Python
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:247:13
    |
245 | # Check Oracle container status
246 | docker ps -a --filter oracle
247 | docker logs oracle-test
    |             ^^^^^^
248 |
249 | # Debug with Python
    |

missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
   --> docs/development.md#block0.py:247:19
    |
245 | # Check Oracle container status
246 | docker ps -a --filter oracle
247 | docker logs oracle-test
    |                   ^
248 |
249 | # Debug with Python
    |
help: Add missing whitespace

missing-whitespace-around-operator: Missing whitespace around operator
   --> docs/development.md#block0.py:250:11
    |
249 | # Debug with Python
250 | PYTHONPATH=src python -c "
    |           ^
251 | from flext_target_oracle import FlextTargetOracleLoader
252 | import logging
    |
help: Add missing whitespace

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:250:16
    |
249 | # Debug with Python
250 | PYTHONPATH=src python -c "
    |                ^^^^^^
251 | from flext_target_oracle import FlextTargetOracleLoader
252 | import logging
    |

missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
   --> docs/development.md#block0.py:250:23
    |
249 | # Debug with Python
250 | PYTHONPATH=src python -c "
    |                       ^
251 | from flext_target_oracle import FlextTargetOracleLoader
252 | import logging
    |
help: Add missing whitespace

invalid-syntax: missing closing quote in string literal
   --> docs/development.md#block0.py:250:26
    |
249 | # Debug with Python
250 | PYTHONPATH=src python -c "
    |                          ^
251 | from flext_target_oracle import FlextTargetOracleLoader
252 | import logging
    |

invalid-syntax: missing closing quote in string literal
   --> docs/development.md#block0.py:256:1
    |
254 | loader = FlextTargetOracleLoader(...)
255 | u.Cli.print('Config created successfully')
256 | "
    | ^
257 | ```
258 | #### 2. Import Errors
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:257:1
    |
255 | u.Cli.print('Config created successfully')
256 | "
257 | ```
    | ^
258 | #### 2. Import Errors
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:257:2
    |
255 | u.Cli.print('Config created successfully')
256 | "
257 | ```
    |  ^
258 | #### 2. Import Errors
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:257:3
    |
255 | u.Cli.print('Config created successfully')
256 | "
257 | ```
    |   ^
258 | #### 2. Import Errors
    |

invalid-syntax: Expected a statement
   --> docs/development.md#block0.py:257:4
    |
255 | u.Cli.print('Config created successfully')
256 | "
257 | ```
    |    ^
258 | #### 2. Import Errors
    |

multiple-leading-hashes-for-block-comment: Too many leading `#` before block comment
   --> docs/development.md#block0.py:258:1
    |
256 | "
257 | ```
258 | #### 2. Import Errors
    | ^^^^^^^^^^^^^^^^^^^^^
259 |
260 | ```text
    |
help: Remove leading `#`

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:260:1
    |
258 | #### 2. Import Errors
259 |
260 | ```text
    | ^
261 | # ❌ Common import issue
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:260:2
    |
258 | #### 2. Import Errors
259 |
260 | ```text
    |  ^
261 | # ❌ Common import issue
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:260:3
    |
258 | #### 2. Import Errors
259 |
260 | ```text
    |   ^
261 | # ❌ Common import issue
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:264:1
    |
263 | # ✅ Check available imports
264 | ```
    | ^
265 |
266 | ```bash
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:264:2
    |
263 | # ✅ Check available imports
264 | ```
    |  ^
265 |
266 | ```bash
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:264:3
    |
263 | # ✅ Check available imports
264 | ```
    |   ^
265 |
266 | ```bash
    |

invalid-syntax: Expected a statement
   --> docs/development.md#block0.py:264:4
    |
263 | # ✅ Check available imports
264 | ```
    |    ^
265 |
266 | ```bash
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:266:1
    |
264 | ```
265 |
266 | ```bash
    | ^
267 | # ✅ Debug imports
268 | python -c "from flext_target_oracle import *; u.Cli.print(dir())"
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:266:2
    |
264 | ```
265 |
266 | ```bash
    |  ^
267 | # ✅ Debug imports
268 | python -c "from flext_target_oracle import *; u.Cli.print(dir())"
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:266:3
    |
264 | ```
265 |
266 | ```bash
    |   ^
267 | # ✅ Debug imports
268 | python -c "from flext_target_oracle import *; u.Cli.print(dir())"
    |

missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
   --> docs/development.md#block0.py:268:8
    |
266 | ```bash
267 | # ✅ Debug imports
268 | python -c "from flext_target_oracle import *; u.Cli.print(dir())"
    |        ^
269 | ```
270 | #### 3. Configuration Validation Errors
    |
help: Add missing whitespace

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:268:11
    |
266 | ```bash
267 | # ✅ Debug imports
268 | python -c "from flext_target_oracle import *; u.Cli.print(dir())"
    |           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
269 | ```
270 | #### 3. Configuration Validation Errors
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:269:1
    |
267 | # ✅ Debug imports
268 | python -c "from flext_target_oracle import *; u.Cli.print(dir())"
269 | ```
    | ^
270 | #### 3. Configuration Validation Errors
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:269:2
    |
267 | # ✅ Debug imports
268 | python -c "from flext_target_oracle import *; u.Cli.print(dir())"
269 | ```
    |  ^
270 | #### 3. Configuration Validation Errors
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:269:3
    |
267 | # ✅ Debug imports
268 | python -c "from flext_target_oracle import *; u.Cli.print(dir())"
269 | ```
    |   ^
270 | #### 3. Configuration Validation Errors
    |

invalid-syntax: Expected a statement
   --> docs/development.md#block0.py:269:4
    |
267 | # ✅ Debug imports
268 | python -c "from flext_target_oracle import *; u.Cli.print(dir())"
269 | ```
    |    ^
270 | #### 3. Configuration Validation Errors
    |

multiple-leading-hashes-for-block-comment: Too many leading `#` before block comment
   --> docs/development.md#block0.py:270:1
    |
268 | python -c "from flext_target_oracle import *; u.Cli.print(dir())"
269 | ```
270 | #### 3. Configuration Validation Errors
    | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
271 |
272 | ```text
    |
help: Remove leading `#`

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:272:1
    |
270 | #### 3. Configuration Validation Errors
271 |
272 | ```text
    | ^
273 | # ❌ Invalid configuration
274 | try:
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:272:2
    |
270 | #### 3. Configuration Validation Errors
271 |
272 | ```text
    |  ^
273 | # ❌ Invalid configuration
274 | try:
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:272:3
    |
270 | #### 3. Configuration Validation Errors
271 |
272 | ```text
    |   ^
273 | # ❌ Invalid configuration
274 | try:
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:286:1
    |
284 | if result.failure:
285 |     u.Cli.print(f"Validation failed: {result.error}")
286 | ```
    | ^
287 | ### Debugging Tools
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:286:2
    |
284 | if result.failure:
285 |     u.Cli.print(f"Validation failed: {result.error}")
286 | ```
    |  ^
287 | ### Debugging Tools
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:286:3
    |
284 | if result.failure:
285 |     u.Cli.print(f"Validation failed: {result.error}")
286 | ```
    |   ^
287 | ### Debugging Tools
    |

invalid-syntax: Expected a statement
   --> docs/development.md#block0.py:286:4
    |
284 | if result.failure:
285 |     u.Cli.print(f"Validation failed: {result.error}")
286 | ```
    |    ^
287 | ### Debugging Tools
    |

multiple-leading-hashes-for-block-comment: Too many leading `#` before block comment
   --> docs/development.md#block0.py:287:1
    |
285 |     u.Cli.print(f"Validation failed: {result.error}")
286 | ```
287 | ### Debugging Tools
    | ^^^^^^^^^^^^^^^^^^^
288 |
289 | #### 1. Enhanced Logging
    |
help: Remove leading `#`

multiple-leading-hashes-for-block-comment: Too many leading `#` before block comment
   --> docs/development.md#block0.py:289:1
    |
287 | ### Debugging Tools
288 |
289 | #### 1. Enhanced Logging
    | ^^^^^^^^^^^^^^^^^^^^^^^^
290 |
291 | ```text
    |
help: Remove leading `#`

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:291:1
    |
289 | #### 1. Enhanced Logging
290 |
291 | ```text
    | ^
292 | # Enable debug logging for development
293 | logging.basicConfig(
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:291:2
    |
289 | #### 1. Enhanced Logging
290 |
291 | ```text
    |  ^
292 | # Enable debug logging for development
293 | logging.basicConfig(
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:291:3
    |
289 | #### 1. Enhanced Logging
290 |
291 | ```text
    |   ^
292 | # Enable debug logging for development
293 | logging.basicConfig(
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:298:1
    |
297 | # FLEXT modules will automatically use debug logging
298 | ```
    | ^
299 | #### 2. Interactive Development
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:298:2
    |
297 | # FLEXT modules will automatically use debug logging
298 | ```
    |  ^
299 | #### 2. Interactive Development
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:298:3
    |
297 | # FLEXT modules will automatically use debug logging
298 | ```
    |   ^
299 | #### 2. Interactive Development
    |

invalid-syntax: Expected a statement
   --> docs/development.md#block0.py:298:4
    |
297 | # FLEXT modules will automatically use debug logging
298 | ```
    |    ^
299 | #### 2. Interactive Development
    |

multiple-leading-hashes-for-block-comment: Too many leading `#` before block comment
   --> docs/development.md#block0.py:299:1
    |
297 | # FLEXT modules will automatically use debug logging
298 | ```
299 | #### 2. Interactive Development
    | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
300 |
301 | ```bash
    |
help: Remove leading `#`

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:301:1
    |
299 | #### 2. Interactive Development
300 |
301 | ```bash
    | ^
302 | # Open Python shell with project context
303 | python -m flext_core.tools.cli
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:301:2
    |
299 | #### 2. Interactive Development
300 |
301 | ```bash
    |  ^
302 | # Open Python shell with project context
303 | python -m flext_core.tools.cli
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:301:3
    |
299 | #### 2. Interactive Development
300 |
301 | ```bash
    |   ^
302 | # Open Python shell with project context
303 | python -m flext_core.tools.cli
    |

missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
   --> docs/development.md#block0.py:303:8
    |
301 | ```bash
302 | # Open Python shell with project context
303 | python -m flext_core.tools.cli
    |        ^
304 |
305 | # In shell:
    |
help: Add missing whitespace

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:303:11
    |
301 | ```bash
302 | # Open Python shell with project context
303 | python -m flext_core.tools.cli
    |           ^^^^^^^^^^
304 |
305 | # In shell:
    |

invalid-syntax: Expected a statement
   --> docs/development.md#block0.py:306:1
    |
305 | # In shell:
306 | >>> from flext_target_oracle import *
    | ^^
307 | >>> # Interactive testing
308 | ```
    |

invalid-syntax: Expected a statement
   --> docs/development.md#block0.py:306:3
    |
305 | # In shell:
306 | >>> from flext_target_oracle import *
    |   ^
307 | >>> # Interactive testing
308 | ```
    |

missing-whitespace-around-operator: Missing whitespace around operator
   --> docs/development.md#block0.py:306:3
    |
305 | # In shell:
306 | >>> from flext_target_oracle import *
    |   ^
307 | >>> # Interactive testing
308 | ```
    |
help: Add missing whitespace

invalid-syntax: Expected a statement
   --> docs/development.md#block0.py:307:1
    |
305 | # In shell:
306 | >>> from flext_target_oracle import *
307 | >>> # Interactive testing
    | ^^
308 | ```
309 | #### 3. Performance Profiling
    |

invalid-syntax: Expected a statement
   --> docs/development.md#block0.py:307:3
    |
305 | # In shell:
306 | >>> from flext_target_oracle import *
307 | >>> # Interactive testing
    |   ^
308 | ```
309 | #### 3. Performance Profiling
    |

missing-whitespace-around-operator: Missing whitespace around operator
   --> docs/development.md#block0.py:307:3
    |
305 | # In shell:
306 | >>> from flext_target_oracle import *
307 | >>> # Interactive testing
    |   ^
308 | ```
309 | #### 3. Performance Profiling
    |
help: Add missing whitespace

too-few-spaces-before-inline-comment: Insert at least two spaces before an inline comment
   --> docs/development.md#block0.py:307:4
    |
305 | # In shell:
306 | >>> from flext_target_oracle import *
307 | >>> # Interactive testing
    |    ^
308 | ```
309 | #### 3. Performance Profiling
    |
help: Insert spaces

invalid-syntax: Expected a statement
   --> docs/development.md#block0.py:307:26
    |
305 | # In shell:
306 | >>> from flext_target_oracle import *
307 | >>> # Interactive testing
    |                          ^
308 | ```
309 | #### 3. Performance Profiling
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:308:1
    |
306 | >>> from flext_target_oracle import *
307 | >>> # Interactive testing
308 | ```
    | ^
309 | #### 3. Performance Profiling
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:308:2
    |
306 | >>> from flext_target_oracle import *
307 | >>> # Interactive testing
308 | ```
    |  ^
309 | #### 3. Performance Profiling
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:308:3
    |
306 | >>> from flext_target_oracle import *
307 | >>> # Interactive testing
308 | ```
    |   ^
309 | #### 3. Performance Profiling
    |

invalid-syntax: Expected a statement
   --> docs/development.md#block0.py:308:4
    |
306 | >>> from flext_target_oracle import *
307 | >>> # Interactive testing
308 | ```
    |    ^
309 | #### 3. Performance Profiling
    |

multiple-leading-hashes-for-block-comment: Too many leading `#` before block comment
   --> docs/development.md#block0.py:309:1
    |
307 | >>> # Interactive testing
308 | ```
309 | #### 3. Performance Profiling
    | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
310 |
311 | ```text
    |
help: Remove leading `#`

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:311:1
    |
309 | #### 3. Performance Profiling
310 |
311 | ```text
    | ^
312 | from __future__ import annotations
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:311:2
    |
309 | #### 3. Performance Profiling
310 |
311 | ```text
    |  ^
312 | from __future__ import annotations
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:311:3
    |
309 | #### 3. Performance Profiling
310 |
311 | ```text
    |   ^
312 | from __future__ import annotations
    |

blank-lines-after-function-or-class: Expected 2 blank lines after class or function definition, found (0)
   --> docs/development.md#block0.py:341:1
    |
339 |     stats.sort_stats("cumulative")
340 |     stats.print_stats(20)  # Top 20 functions by time
341 | ```
    | ^
342 | ## Testing Development
    |
help: Add missing blank line(s)

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:341:1
    |
339 |     stats.sort_stats("cumulative")
340 |     stats.print_stats(20)  # Top 20 functions by time
341 | ```
    | ^
342 | ## Testing Development
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:341:2
    |
339 |     stats.sort_stats("cumulative")
340 |     stats.print_stats(20)  # Top 20 functions by time
341 | ```
    |  ^
342 | ## Testing Development
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:341:3
    |
339 |     stats.sort_stats("cumulative")
340 |     stats.print_stats(20)  # Top 20 functions by time
341 | ```
    |   ^
342 | ## Testing Development
    |

invalid-syntax: Expected a statement
   --> docs/development.md#block0.py:341:4
    |
339 |     stats.sort_stats("cumulative")
340 |     stats.print_stats(20)  # Top 20 functions by time
341 | ```
    |    ^
342 | ## Testing Development
    |

multiple-leading-hashes-for-block-comment: Too many leading `#` before block comment
   --> docs/development.md#block0.py:342:1
    |
340 |     stats.print_stats(20)  # Top 20 functions by time
341 | ```
342 | ## Testing Development
    | ^^^^^^^^^^^^^^^^^^^^^^
343 |
344 | ### Writing New Tests
    |
help: Remove leading `#`

multiple-leading-hashes-for-block-comment: Too many leading `#` before block comment
   --> docs/development.md#block0.py:344:1
    |
342 | ## Testing Development
343 |
344 | ### Writing New Tests
    | ^^^^^^^^^^^^^^^^^^^^^
345 |
346 | #### Unit Test Template
    |
help: Remove leading `#`

multiple-leading-hashes-for-block-comment: Too many leading `#` before block comment
   --> docs/development.md#block0.py:346:1
    |
344 | ### Writing New Tests
345 |
346 | #### Unit Test Template
    | ^^^^^^^^^^^^^^^^^^^^^^^
347 |
348 | ```text
    |
help: Remove leading `#`

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:348:1
    |
346 | #### Unit Test Template
347 |
348 | ```text
    | ^
349 | """Test template for new functionality."""
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:348:2
    |
346 | #### Unit Test Template
347 |
348 | ```text
    |  ^
349 | """Test template for new functionality."""
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:348:3
    |
346 | #### Unit Test Template
347 |
348 | ```text
    |   ^
349 | """Test template for new functionality."""
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:404:1
    |
402 |         result = operation(input_value)
403 |         tm.that(result, eq=expected)
404 | ```
    | ^
405 | #### Integration Test Template
    |

blank-lines-after-function-or-class: Expected 2 blank lines after class or function definition, found (0)
   --> docs/development.md#block0.py:404:1
    |
402 |         result = operation(input_value)
403 |         tm.that(result, eq=expected)
404 | ```
    | ^
405 | #### Integration Test Template
    |
help: Add missing blank line(s)

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:404:2
    |
402 |         result = operation(input_value)
403 |         tm.that(result, eq=expected)
404 | ```
    |  ^
405 | #### Integration Test Template
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:404:3
    |
402 |         result = operation(input_value)
403 |         tm.that(result, eq=expected)
404 | ```
    |   ^
405 | #### Integration Test Template
    |

invalid-syntax: Expected a statement
   --> docs/development.md#block0.py:404:4
    |
402 |         result = operation(input_value)
403 |         tm.that(result, eq=expected)
404 | ```
    |    ^
405 | #### Integration Test Template
    |

multiple-leading-hashes-for-block-comment: Too many leading `#` before block comment
   --> docs/development.md#block0.py:405:1
    |
403 |         tm.that(result, eq=expected)
404 | ```
405 | #### Integration Test Template
    | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
406 |
407 | ```text
    |
help: Remove leading `#`

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:407:1
    |
405 | #### Integration Test Template
406 |
407 | ```text
    | ^
408 | from __future__ import annotations
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:407:2
    |
405 | #### Integration Test Template
406 |
407 | ```text
    |  ^
408 | from __future__ import annotations
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:407:3
    |
405 | #### Integration Test Template
406 |
407 | ```text
    |   ^
408 | from __future__ import annotations
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:439:1
    |
437 |         result = oracle_loader.load_record("test_stream", {...})
438 |         tm.ok(result.success)
439 | ```
    | ^
440 | ### Test Data Management
    |

blank-lines-after-function-or-class: Expected 2 blank lines after class or function definition, found (0)
   --> docs/development.md#block0.py:439:1
    |
437 |         result = oracle_loader.load_record("test_stream", {...})
438 |         tm.ok(result.success)
439 | ```
    | ^
440 | ### Test Data Management
    |
help: Add missing blank line(s)

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:439:2
    |
437 |         result = oracle_loader.load_record("test_stream", {...})
438 |         tm.ok(result.success)
439 | ```
    |  ^
440 | ### Test Data Management
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:439:3
    |
437 |         result = oracle_loader.load_record("test_stream", {...})
438 |         tm.ok(result.success)
439 | ```
    |   ^
440 | ### Test Data Management
    |

invalid-syntax: Expected a statement
   --> docs/development.md#block0.py:439:4
    |
437 |         result = oracle_loader.load_record("test_stream", {...})
438 |         tm.ok(result.success)
439 | ```
    |    ^
440 | ### Test Data Management
    |

multiple-leading-hashes-for-block-comment: Too many leading `#` before block comment
   --> docs/development.md#block0.py:440:1
    |
438 |         tm.ok(result.success)
439 | ```
440 | ### Test Data Management
    | ^^^^^^^^^^^^^^^^^^^^^^^^
441 |
442 | ```text
    |
help: Remove leading `#`

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:442:1
    |
440 | ### Test Data Management
441 |
442 | ```text
    | ^
443 | from __future__ import annotations
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:442:2
    |
440 | ### Test Data Management
441 |
442 | ```text
    |  ^
443 | from __future__ import annotations
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:442:3
    |
440 | ### Test Data Management
441 |
442 | ```text
    |   ^
443 | from __future__ import annotations
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:476:1
    |
474 |         {"id": 2, "name": "Jane Smith", "email": "jane@example.com"},
475 |     ]
476 | ```
    | ^
477 | ## Performance Development
    |

blank-lines-after-function-or-class: Expected 2 blank lines after class or function definition, found (0)
   --> docs/development.md#block0.py:476:1
    |
474 |         {"id": 2, "name": "Jane Smith", "email": "jane@example.com"},
475 |     ]
476 | ```
    | ^
477 | ## Performance Development
    |
help: Add missing blank line(s)

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:476:2
    |
474 |         {"id": 2, "name": "Jane Smith", "email": "jane@example.com"},
475 |     ]
476 | ```
    |  ^
477 | ## Performance Development
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:476:3
    |
474 |         {"id": 2, "name": "Jane Smith", "email": "jane@example.com"},
475 |     ]
476 | ```
    |   ^
477 | ## Performance Development
    |

invalid-syntax: Expected a statement
   --> docs/development.md#block0.py:476:4
    |
474 |         {"id": 2, "name": "Jane Smith", "email": "jane@example.com"},
475 |     ]
476 | ```
    |    ^
477 | ## Performance Development
    |

multiple-leading-hashes-for-block-comment: Too many leading `#` before block comment
   --> docs/development.md#block0.py:477:1
    |
475 |     ]
476 | ```
477 | ## Performance Development
    | ^^^^^^^^^^^^^^^^^^^^^^^^^^
478 |
479 | ### Batch Size Optimization
    |
help: Remove leading `#`

multiple-leading-hashes-for-block-comment: Too many leading `#` before block comment
   --> docs/development.md#block0.py:479:1
    |
477 | ## Performance Development
478 |
479 | ### Batch Size Optimization
    | ^^^^^^^^^^^^^^^^^^^^^^^^^^^
480 |
481 | ```text
    |
help: Remove leading `#`

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:481:1
    |
479 | ### Batch Size Optimization
480 |
481 | ```text
    | ^
482 | from __future__ import annotations
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:481:2
    |
479 | ### Batch Size Optimization
480 |
481 | ```text
    |  ^
482 | from __future__ import annotations
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:481:3
    |
479 | ### Batch Size Optimization
480 |
481 | ```text
    |   ^
482 | from __future__ import annotations
    |

blank-lines-after-function-or-class: Expected 2 blank lines after class or function definition, found (0)
   --> docs/development.md#block0.py:525:1
    |
523 |             f"Batch size {batch_size}: {stats['records_per_second']:.1f} records/sec"
524 |         )
525 | ```
    | ^
526 | ### Memory Usage Monitoring
    |
help: Add missing blank line(s)

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:525:1
    |
523 |             f"Batch size {batch_size}: {stats['records_per_second']:.1f} records/sec"
524 |         )
525 | ```
    | ^
526 | ### Memory Usage Monitoring
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:525:2
    |
523 |             f"Batch size {batch_size}: {stats['records_per_second']:.1f} records/sec"
524 |         )
525 | ```
    |  ^
526 | ### Memory Usage Monitoring
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:525:3
    |
523 |             f"Batch size {batch_size}: {stats['records_per_second']:.1f} records/sec"
524 |         )
525 | ```
    |   ^
526 | ### Memory Usage Monitoring
    |

invalid-syntax: Expected a statement
   --> docs/development.md#block0.py:525:4
    |
523 |             f"Batch size {batch_size}: {stats['records_per_second']:.1f} records/sec"
524 |         )
525 | ```
    |    ^
526 | ### Memory Usage Monitoring
    |

multiple-leading-hashes-for-block-comment: Too many leading `#` before block comment
   --> docs/development.md#block0.py:526:1
    |
524 |         )
525 | ```
526 | ### Memory Usage Monitoring
    | ^^^^^^^^^^^^^^^^^^^^^^^^^^^
527 |
528 | ```text
    |
help: Remove leading `#`

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:528:1
    |
526 | ### Memory Usage Monitoring
527 |
528 | ```text
    | ^
529 | from __future__ import annotations
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:528:2
    |
526 | ### Memory Usage Monitoring
527 |
528 | ```text
    |  ^
529 | from __future__ import annotations
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:528:3
    |
526 | ### Memory Usage Monitoring
527 |
528 | ```text
    |   ^
529 | from __future__ import annotations
    |

blank-lines-after-function-or-class: Expected 2 blank lines after class or function definition, found (0)
   --> docs/development.md#block0.py:558:1
    |
557 |     u.Cli.print(f"Final memory: {get_memory_mb():.1f} MB")
558 | ```
    | ^
559 | ## Contributing Guidelines
    |
help: Add missing blank line(s)

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:558:1
    |
557 |     u.Cli.print(f"Final memory: {get_memory_mb():.1f} MB")
558 | ```
    | ^
559 | ## Contributing Guidelines
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:558:2
    |
557 |     u.Cli.print(f"Final memory: {get_memory_mb():.1f} MB")
558 | ```
    |  ^
559 | ## Contributing Guidelines
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:558:3
    |
557 |     u.Cli.print(f"Final memory: {get_memory_mb():.1f} MB")
558 | ```
    |   ^
559 | ## Contributing Guidelines
    |

invalid-syntax: Expected a statement
   --> docs/development.md#block0.py:558:4
    |
557 |     u.Cli.print(f"Final memory: {get_memory_mb():.1f} MB")
558 | ```
    |    ^
559 | ## Contributing Guidelines
    |

multiple-leading-hashes-for-block-comment: Too many leading `#` before block comment
   --> docs/development.md#block0.py:559:1
    |
557 |     u.Cli.print(f"Final memory: {get_memory_mb():.1f} MB")
558 | ```
559 | ## Contributing Guidelines
    | ^^^^^^^^^^^^^^^^^^^^^^^^^^
560 |
561 | ### Pull Request Checklist
    |
help: Remove leading `#`

multiple-leading-hashes-for-block-comment: Too many leading `#` before block comment
   --> docs/development.md#block0.py:561:1
    |
559 | ## Contributing Guidelines
560 |
561 | ### Pull Request Checklist
    | ^^^^^^^^^^^^^^^^^^^^^^^^^^
562 |
563 | Before submitting a pull request:
    |
help: Remove leading `#`

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:563:8
    |
561 | ### Pull Request Checklist
562 |
563 | Before submitting a pull request:
    |        ^^^^^^^^^^
564 |
565 | - [ ] **Code Quality**: `make check` passes with zero issues
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:563:19
    |
561 | ### Pull Request Checklist
562 |
563 | Before submitting a pull request:
    |                   ^
564 |
565 | - [ ] **Code Quality**: `make check` passes with zero issues
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:563:21
    |
561 | ### Pull Request Checklist
562 |
563 | Before submitting a pull request:
    |                     ^^^^
564 |
565 | - [ ] **Code Quality**: `make check` passes with zero issues
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:563:26
    |
561 | ### Pull Request Checklist
562 |
563 | Before submitting a pull request:
    |                          ^^^^^^^
564 |
565 | - [ ] **Code Quality**: `make check` passes with zero issues
    |

invalid-syntax: Expected an expression
   --> docs/development.md#block0.py:563:34
    |
561 | ### Pull Request Checklist
562 |
563 | Before submitting a pull request:
    |                                  ^
564 |
565 | - [ ] **Code Quality**: `make check` passes with zero issues
    |

no-indented-block: Expected an indented block
   --> docs/development.md#block0.py:565:1
    |
563 | Before submitting a pull request:
564 |
565 | - [ ] **Code Quality**: `make check` passes with zero issues
    | ^
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
    |

whitespace-after-open-bracket: Whitespace after '['
   --> docs/development.md#block0.py:565:4
    |
563 | Before submitting a pull request:
564 |
565 | - [ ] **Code Quality**: `make check` passes with zero issues
    |    ^
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
    |
help: Remove whitespace before '['

whitespace-before-close-bracket: Whitespace before ']'
   --> docs/development.md#block0.py:565:4
    |
563 | Before submitting a pull request:
564 |
565 | - [ ] **Code Quality**: `make check` passes with zero issues
    |    ^
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
    |
help: Remove whitespace before ']'

missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
   --> docs/development.md#block0.py:565:7
    |
563 | Before submitting a pull request:
564 |
565 | - [ ] **Code Quality**: `make check` passes with zero issues
    |       ^^
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
    |
help: Add missing whitespace

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:565:14
    |
563 | Before submitting a pull request:
564 |
565 | - [ ] **Code Quality**: `make check` passes with zero issues
    |              ^^^^^^^
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
    |

invalid-syntax: Invalid annotated assignment target
   --> docs/development.md#block0.py:565:14
    |
563 | Before submitting a pull request:
564 |
565 | - [ ] **Code Quality**: `make check` passes with zero issues
    |              ^^^^^^^^^
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
    |

invalid-syntax: Expected an expression
   --> docs/development.md#block0.py:565:23
    |
563 | Before submitting a pull request:
564 |
565 | - [ ] **Code Quality**: `make check` passes with zero issues
    |                       ^
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:565:25
    |
563 | Before submitting a pull request:
564 |
565 | - [ ] **Code Quality**: `make check` passes with zero issues
    |                         ^
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:565:31
    |
563 | Before submitting a pull request:
564 |
565 | - [ ] **Code Quality**: `make check` passes with zero issues
    |                               ^^^^^
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:565:36
    |
563 | Before submitting a pull request:
564 |
565 | - [ ] **Code Quality**: `make check` passes with zero issues
    |                                    ^
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
    |

invalid-syntax: Compound statements are not allowed on the same line as simple statements
   --> docs/development.md#block0.py:565:45
    |
563 | Before submitting a pull request:
564 |
565 | - [ ] **Code Quality**: `make check` passes with zero issues
    |                                             ^^^^
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
    |

invalid-syntax: Expected `,`, found identifier
   --> docs/development.md#block0.py:565:55
    |
563 | Before submitting a pull request:
564 |
565 | - [ ] **Code Quality**: `make check` passes with zero issues
    |                                                       ^^^^^^
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
    |

invalid-syntax: Expected `:`, found newline
   --> docs/development.md#block0.py:565:61
    |
563 | Before submitting a pull request:
564 |
565 | - [ ] **Code Quality**: `make check` passes with zero issues
    |                                                             ^
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
    |

invalid-syntax: Expected an indented block after `with` statement
   --> docs/development.md#block0.py:566:1
    |
565 | - [ ] **Code Quality**: `make check` passes with zero issues
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
    | ^
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
568 | - [ ] **Security**: No new security vulnerabilities introduced
    |

invalid-syntax: Invalid annotated assignment target
   --> docs/development.md#block0.py:566:1
    |
565 | - [ ] **Code Quality**: `make check` passes with zero issues
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
    | ^^^^^^^^^^^^^^^
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
568 | - [ ] **Security**: No new security vulnerabilities introduced
    |

whitespace-after-open-bracket: Whitespace after '['
   --> docs/development.md#block0.py:566:4
    |
565 | - [ ] **Code Quality**: `make check` passes with zero issues
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
    |    ^
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
568 | - [ ] **Security**: No new security vulnerabilities introduced
    |
help: Remove whitespace before '['

whitespace-before-close-bracket: Whitespace before ']'
   --> docs/development.md#block0.py:566:4
    |
565 | - [ ] **Code Quality**: `make check` passes with zero issues
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
    |    ^
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
568 | - [ ] **Security**: No new security vulnerabilities introduced
    |
help: Remove whitespace before ']'

missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
   --> docs/development.md#block0.py:566:7
    |
565 | - [ ] **Code Quality**: `make check` passes with zero issues
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
    |       ^^
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
568 | - [ ] **Security**: No new security vulnerabilities introduced
    |
help: Add missing whitespace

invalid-syntax: Expected an expression
   --> docs/development.md#block0.py:566:16
    |
565 | - [ ] **Code Quality**: `make check` passes with zero issues
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
    |                ^
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
568 | - [ ] **Security**: No new security vulnerabilities introduced
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:566:22
    |
565 | - [ ] **Code Quality**: `make check` passes with zero issues
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
    |                      ^^^^^^^^
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
568 | - [ ] **Security**: No new security vulnerabilities introduced
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:566:31
    |
565 | - [ ] **Code Quality**: `make check` passes with zero issues
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
    |                               ^^^^^
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
568 | - [ ] **Security**: No new security vulnerabilities introduced
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:566:37
    |
565 | - [ ] **Code Quality**: `make check` passes with zero issues
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
    |                                     ^^^^
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
568 | - [ ] **Security**: No new security vulnerabilities introduced
    |

missing-whitespace-after-keyword: Missing whitespace after keyword
   --> docs/development.md#block0.py:566:37
    |
565 | - [ ] **Code Quality**: `make check` passes with zero issues
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
    |                                     ^^^^
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
568 | - [ ] **Security**: No new security vulnerabilities introduced
    |
help: Added missing whitespace after keyword

invalid-syntax: Expected a statement
   --> docs/development.md#block0.py:566:41
    |
565 | - [ ] **Code Quality**: `make check` passes with zero issues
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
    |                                         ^
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
568 | - [ ] **Security**: No new security vulnerabilities introduced
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:566:47
    |
565 | - [ ] **Code Quality**: `make check` passes with zero issues
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
    |                                               ^^^^^
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
568 | - [ ] **Security**: No new security vulnerabilities introduced
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:566:53
    |
565 | - [ ] **Code Quality**: `make check` passes with zero issues
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
    |                                                     ^^^^^
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
568 | - [ ] **Security**: No new security vulnerabilities introduced
    |

invalid-syntax: Compound statements are not allowed on the same line as simple statements
   --> docs/development.md#block0.py:566:59
    |
565 | - [ ] **Code Quality**: `make check` passes with zero issues
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
    |                                                           ^^^
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
568 | - [ ] **Security**: No new security vulnerabilities introduced
    |

invalid-syntax: Expected `in`, found identifier
   --> docs/development.md#block0.py:566:67
    |
565 | - [ ] **Code Quality**: `make check` passes with zero issues
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
    |                                                                   ^^^^^^^^^^^^^
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
568 | - [ ] **Security**: No new security vulnerabilities introduced
    |

invalid-syntax: Expected `:`, found newline
   --> docs/development.md#block0.py:566:80
    |
565 | - [ ] **Code Quality**: `make check` passes with zero issues
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
    |                                                                                ^
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
568 | - [ ] **Security**: No new security vulnerabilities introduced
    |

invalid-syntax: Expected an indented block after `for` statement
   --> docs/development.md#block0.py:567:1
    |
565 | - [ ] **Code Quality**: `make check` passes with zero issues
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
    | ^
568 | - [ ] **Security**: No new security vulnerabilities introduced
569 | - [ ] **FLEXT Patterns**: Follows established FLEXT ecosystem patterns
    |

invalid-syntax: Invalid annotated assignment target
   --> docs/development.md#block0.py:567:1
    |
565 | - [ ] **Code Quality**: `make check` passes with zero issues
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
    | ^^^^^^^^^^^^^^^^^^^^^^^
568 | - [ ] **Security**: No new security vulnerabilities introduced
569 | - [ ] **FLEXT Patterns**: Follows established FLEXT ecosystem patterns
    |

whitespace-after-open-bracket: Whitespace after '['
   --> docs/development.md#block0.py:567:4
    |
565 | - [ ] **Code Quality**: `make check` passes with zero issues
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
    |    ^
568 | - [ ] **Security**: No new security vulnerabilities introduced
569 | - [ ] **FLEXT Patterns**: Follows established FLEXT ecosystem patterns
    |
help: Remove whitespace before '['

whitespace-before-close-bracket: Whitespace before ']'
   --> docs/development.md#block0.py:567:4
    |
565 | - [ ] **Code Quality**: `make check` passes with zero issues
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
    |    ^
568 | - [ ] **Security**: No new security vulnerabilities introduced
569 | - [ ] **FLEXT Patterns**: Follows established FLEXT ecosystem patterns
    |
help: Remove whitespace before ']'

missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
   --> docs/development.md#block0.py:567:7
    |
565 | - [ ] **Code Quality**: `make check` passes with zero issues
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
    |       ^^
568 | - [ ] **Security**: No new security vulnerabilities introduced
569 | - [ ] **FLEXT Patterns**: Follows established FLEXT ecosystem patterns
    |
help: Add missing whitespace

invalid-syntax: Expected an expression
   --> docs/development.md#block0.py:567:24
    |
565 | - [ ] **Code Quality**: `make check` passes with zero issues
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
    |                        ^
568 | - [ ] **Security**: No new security vulnerabilities introduced
569 | - [ ] **FLEXT Patterns**: Follows established FLEXT ecosystem patterns
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:567:34
    |
565 | - [ ] **Code Quality**: `make check` passes with zero issues
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
    |                                  ^^^^^^^^
568 | - [ ] **Security**: No new security vulnerabilities introduced
569 | - [ ] **FLEXT Patterns**: Follows established FLEXT ecosystem patterns
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:567:43
    |
565 | - [ ] **Code Quality**: `make check` passes with zero issues
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
    |                                           ^^^^^^^^^^^^^
568 | - [ ] **Security**: No new security vulnerabilities introduced
569 | - [ ] **FLEXT Patterns**: Follows established FLEXT ecosystem patterns
    |

whitespace-before-parameters: Whitespace before '('
   --> docs/development.md#block0.py:567:56
    |
565 | - [ ] **Code Quality**: `make check` passes with zero issues
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
    |                                                        ^
568 | - [ ] **Security**: No new security vulnerabilities introduced
569 | - [ ] **FLEXT Patterns**: Follows established FLEXT ecosystem patterns
    |
help: Removed whitespace before '('

invalid-syntax: Invalid annotated assignment target
   --> docs/development.md#block0.py:568:1
    |
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
568 | - [ ] **Security**: No new security vulnerabilities introduced
    | ^^^^^^^^^^^^^^^^^^
569 | - [ ] **FLEXT Patterns**: Follows established FLEXT ecosystem patterns
570 | - [ ] **Backward Compatibility**: No breaking changes without major version bump
    |

whitespace-after-open-bracket: Whitespace after '['
   --> docs/development.md#block0.py:568:4
    |
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
568 | - [ ] **Security**: No new security vulnerabilities introduced
    |    ^
569 | - [ ] **FLEXT Patterns**: Follows established FLEXT ecosystem patterns
570 | - [ ] **Backward Compatibility**: No breaking changes without major version bump
    |
help: Remove whitespace before '['

whitespace-before-close-bracket: Whitespace before ']'
   --> docs/development.md#block0.py:568:4
    |
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
568 | - [ ] **Security**: No new security vulnerabilities introduced
    |    ^
569 | - [ ] **FLEXT Patterns**: Follows established FLEXT ecosystem patterns
570 | - [ ] **Backward Compatibility**: No breaking changes without major version bump
    |
help: Remove whitespace before ']'

missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
   --> docs/development.md#block0.py:568:7
    |
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
568 | - [ ] **Security**: No new security vulnerabilities introduced
    |       ^^
569 | - [ ] **FLEXT Patterns**: Follows established FLEXT ecosystem patterns
570 | - [ ] **Backward Compatibility**: No breaking changes without major version bump
    |
help: Add missing whitespace

invalid-syntax: Expected an expression
   --> docs/development.md#block0.py:568:19
    |
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
568 | - [ ] **Security**: No new security vulnerabilities introduced
    |                   ^
569 | - [ ] **FLEXT Patterns**: Follows established FLEXT ecosystem patterns
570 | - [ ] **Backward Compatibility**: No breaking changes without major version bump
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:568:24
    |
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
568 | - [ ] **Security**: No new security vulnerabilities introduced
    |                        ^^^
569 | - [ ] **FLEXT Patterns**: Follows established FLEXT ecosystem patterns
570 | - [ ] **Backward Compatibility**: No breaking changes without major version bump
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:568:28
    |
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
568 | - [ ] **Security**: No new security vulnerabilities introduced
    |                            ^^^^^^^^
569 | - [ ] **FLEXT Patterns**: Follows established FLEXT ecosystem patterns
570 | - [ ] **Backward Compatibility**: No breaking changes without major version bump
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:568:37
    |
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
568 | - [ ] **Security**: No new security vulnerabilities introduced
    |                                     ^^^^^^^^^^^^^^^
569 | - [ ] **FLEXT Patterns**: Follows established FLEXT ecosystem patterns
570 | - [ ] **Backward Compatibility**: No breaking changes without major version bump
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:568:53
    |
566 | - [ ] **Tests**: All existing tests pass, new tests added for new functionality
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
568 | - [ ] **Security**: No new security vulnerabilities introduced
    |                                                     ^^^^^^^^^^
569 | - [ ] **FLEXT Patterns**: Follows established FLEXT ecosystem patterns
570 | - [ ] **Backward Compatibility**: No breaking changes without major version bump
    |

whitespace-after-open-bracket: Whitespace after '['
   --> docs/development.md#block0.py:569:4
    |
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
568 | - [ ] **Security**: No new security vulnerabilities introduced
569 | - [ ] **FLEXT Patterns**: Follows established FLEXT ecosystem patterns
    |    ^
570 | - [ ] **Backward Compatibility**: No breaking changes without major version bump
    |
help: Remove whitespace before '['

whitespace-before-close-bracket: Whitespace before ']'
   --> docs/development.md#block0.py:569:4
    |
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
568 | - [ ] **Security**: No new security vulnerabilities introduced
569 | - [ ] **FLEXT Patterns**: Follows established FLEXT ecosystem patterns
    |    ^
570 | - [ ] **Backward Compatibility**: No breaking changes without major version bump
    |
help: Remove whitespace before ']'

missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
   --> docs/development.md#block0.py:569:7
    |
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
568 | - [ ] **Security**: No new security vulnerabilities introduced
569 | - [ ] **FLEXT Patterns**: Follows established FLEXT ecosystem patterns
    |       ^^
570 | - [ ] **Backward Compatibility**: No breaking changes without major version bump
    |
help: Add missing whitespace

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:569:15
    |
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
568 | - [ ] **Security**: No new security vulnerabilities introduced
569 | - [ ] **FLEXT Patterns**: Follows established FLEXT ecosystem patterns
    |               ^^^^^^^^
570 | - [ ] **Backward Compatibility**: No breaking changes without major version bump
    |

invalid-syntax: Invalid annotated assignment target
   --> docs/development.md#block0.py:569:15
    |
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
568 | - [ ] **Security**: No new security vulnerabilities introduced
569 | - [ ] **FLEXT Patterns**: Follows established FLEXT ecosystem patterns
    |               ^^^^^^^^^^
570 | - [ ] **Backward Compatibility**: No breaking changes without major version bump
    |

invalid-syntax: Expected an expression
   --> docs/development.md#block0.py:569:25
    |
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
568 | - [ ] **Security**: No new security vulnerabilities introduced
569 | - [ ] **FLEXT Patterns**: Follows established FLEXT ecosystem patterns
    |                         ^
570 | - [ ] **Backward Compatibility**: No breaking changes without major version bump
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:569:35
    |
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
568 | - [ ] **Security**: No new security vulnerabilities introduced
569 | - [ ] **FLEXT Patterns**: Follows established FLEXT ecosystem patterns
    |                                   ^^^^^^^^^^^
570 | - [ ] **Backward Compatibility**: No breaking changes without major version bump
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:569:47
    |
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
568 | - [ ] **Security**: No new security vulnerabilities introduced
569 | - [ ] **FLEXT Patterns**: Follows established FLEXT ecosystem patterns
    |                                               ^^^^^
570 | - [ ] **Backward Compatibility**: No breaking changes without major version bump
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:569:53
    |
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
568 | - [ ] **Security**: No new security vulnerabilities introduced
569 | - [ ] **FLEXT Patterns**: Follows established FLEXT ecosystem patterns
    |                                                     ^^^^^^^^^
570 | - [ ] **Backward Compatibility**: No breaking changes without major version bump
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:569:63
    |
567 | - [ ] **Documentation**: Updated relevant documentation (architecture, API)
568 | - [ ] **Security**: No new security vulnerabilities introduced
569 | - [ ] **FLEXT Patterns**: Follows established FLEXT ecosystem patterns
    |                                                               ^^^^^^^^
570 | - [ ] **Backward Compatibility**: No breaking changes without major version bump
    |

whitespace-after-open-bracket: Whitespace after '['
   --> docs/development.md#block0.py:570:4
    |
568 | - [ ] **Security**: No new security vulnerabilities introduced
569 | - [ ] **FLEXT Patterns**: Follows established FLEXT ecosystem patterns
570 | - [ ] **Backward Compatibility**: No breaking changes without major version bump
    |    ^
571 |
572 | ### Commit Message Format
    |
help: Remove whitespace before '['

whitespace-before-close-bracket: Whitespace before ']'
   --> docs/development.md#block0.py:570:4
    |
568 | - [ ] **Security**: No new security vulnerabilities introduced
569 | - [ ] **FLEXT Patterns**: Follows established FLEXT ecosystem patterns
570 | - [ ] **Backward Compatibility**: No breaking changes without major version bump
    |    ^
571 |
572 | ### Commit Message Format
    |
help: Remove whitespace before ']'

missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
   --> docs/development.md#block0.py:570:7
    |
568 | - [ ] **Security**: No new security vulnerabilities introduced
569 | - [ ] **FLEXT Patterns**: Follows established FLEXT ecosystem patterns
570 | - [ ] **Backward Compatibility**: No breaking changes without major version bump
    |       ^^
571 |
572 | ### Commit Message Format
    |
help: Add missing whitespace

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:570:18
    |
568 | - [ ] **Security**: No new security vulnerabilities introduced
569 | - [ ] **FLEXT Patterns**: Follows established FLEXT ecosystem patterns
570 | - [ ] **Backward Compatibility**: No breaking changes without major version bump
    |                  ^^^^^^^^^^^^^
571 |
572 | ### Commit Message Format
    |

invalid-syntax: Invalid annotated assignment target
   --> docs/development.md#block0.py:570:18
    |
568 | - [ ] **Security**: No new security vulnerabilities introduced
569 | - [ ] **FLEXT Patterns**: Follows established FLEXT ecosystem patterns
570 | - [ ] **Backward Compatibility**: No breaking changes without major version bump
    |                  ^^^^^^^^^^^^^^^
571 |
572 | ### Commit Message Format
    |

invalid-syntax: Expected an expression
   --> docs/development.md#block0.py:570:33
    |
568 | - [ ] **Security**: No new security vulnerabilities introduced
569 | - [ ] **FLEXT Patterns**: Follows established FLEXT ecosystem patterns
570 | - [ ] **Backward Compatibility**: No breaking changes without major version bump
    |                                 ^
571 |
572 | ### Commit Message Format
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:570:38
    |
568 | - [ ] **Security**: No new security vulnerabilities introduced
569 | - [ ] **FLEXT Patterns**: Follows established FLEXT ecosystem patterns
570 | - [ ] **Backward Compatibility**: No breaking changes without major version bump
    |                                      ^^^^^^^^
571 |
572 | ### Commit Message Format
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:570:47
    |
568 | - [ ] **Security**: No new security vulnerabilities introduced
569 | - [ ] **FLEXT Patterns**: Follows established FLEXT ecosystem patterns
570 | - [ ] **Backward Compatibility**: No breaking changes without major version bump
    |                                               ^^^^^^^
571 |
572 | ### Commit Message Format
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:570:55
    |
568 | - [ ] **Security**: No new security vulnerabilities introduced
569 | - [ ] **FLEXT Patterns**: Follows established FLEXT ecosystem patterns
570 | - [ ] **Backward Compatibility**: No breaking changes without major version bump
    |                                                       ^^^^^^^
571 |
572 | ### Commit Message Format
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:570:63
    |
568 | - [ ] **Security**: No new security vulnerabilities introduced
569 | - [ ] **FLEXT Patterns**: Follows established FLEXT ecosystem patterns
570 | - [ ] **Backward Compatibility**: No breaking changes without major version bump
    |                                                               ^^^^^
571 |
572 | ### Commit Message Format
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:570:69
    |
568 | - [ ] **Security**: No new security vulnerabilities introduced
569 | - [ ] **FLEXT Patterns**: Follows established FLEXT ecosystem patterns
570 | - [ ] **Backward Compatibility**: No breaking changes without major version bump
    |                                                                     ^^^^^^^
571 |
572 | ### Commit Message Format
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:570:77
    |
568 | - [ ] **Security**: No new security vulnerabilities introduced
569 | - [ ] **FLEXT Patterns**: Follows established FLEXT ecosystem patterns
570 | - [ ] **Backward Compatibility**: No breaking changes without major version bump
    |                                                                             ^^^^
571 |
572 | ### Commit Message Format
    |

multiple-leading-hashes-for-block-comment: Too many leading `#` before block comment
   --> docs/development.md#block0.py:572:1
    |
570 | - [ ] **Backward Compatibility**: No breaking changes without major version bump
571 |
572 | ### Commit Message Format
    | ^^^^^^^^^^^^^^^^^^^^^^^^^
573 | ```
574 | type(scope): brief description
    |
help: Remove leading `#`

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:573:1
    |
572 | ### Commit Message Format
573 | ```
    | ^
574 | type(scope): brief description
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:573:2
    |
572 | ### Commit Message Format
573 | ```
    |  ^
574 | type(scope): brief description
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:573:3
    |
572 | ### Commit Message Format
573 | ```
    |   ^
574 | type(scope): brief description
    |

invalid-syntax: Expected a statement
   --> docs/development.md#block0.py:573:4
    |
572 | ### Commit Message Format
573 | ```
    |    ^
574 | type(scope): brief description
    |

invalid-syntax: Invalid annotated assignment target
   --> docs/development.md#block0.py:574:1
    |
572 | ### Commit Message Format
573 | ```
574 | type(scope): brief description
    | ^^^^^^^^^^^
575 |
576 | Detailed explanation of changes made, why they were necessary,
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:574:20
    |
572 | ### Commit Message Format
573 | ```
574 | type(scope): brief description
    |                    ^^^^^^^^^^^
575 |
576 | Detailed explanation of changes made, why they were necessary,
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:576:10
    |
574 | type(scope): brief description
575 |
576 | Detailed explanation of changes made, why they were necessary,
    |          ^^^^^^^^^^^
577 | and any breaking changes introduced.
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:576:22
    |
574 | type(scope): brief description
575 |
576 | Detailed explanation of changes made, why they were necessary,
    |                      ^^
577 | and any breaking changes introduced.
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:576:25
    |
574 | type(scope): brief description
575 |
576 | Detailed explanation of changes made, why they were necessary,
    |                         ^^^^^^^
577 | and any breaking changes introduced.
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:576:33
    |
574 | type(scope): brief description
575 |
576 | Detailed explanation of changes made, why they were necessary,
    |                                 ^^^^
577 | and any breaking changes introduced.
    |

invalid-syntax: Expected `,`, found identifier
   --> docs/development.md#block0.py:576:43
    |
574 | type(scope): brief description
575 |
576 | Detailed explanation of changes made, why they were necessary,
    |                                           ^^^^
577 | and any breaking changes introduced.
    |

invalid-syntax: Expected `,`, found identifier
   --> docs/development.md#block0.py:576:48
    |
574 | type(scope): brief description
575 |
576 | Detailed explanation of changes made, why they were necessary,
    |                                                ^^^^
577 | and any breaking changes introduced.
    |

invalid-syntax: Expected `,`, found identifier
   --> docs/development.md#block0.py:576:53
    |
574 | type(scope): brief description
575 |
576 | Detailed explanation of changes made, why they were necessary,
    |                                                     ^^^^^^^^^
577 | and any breaking changes introduced.
    |

trailing-comma-on-bare-tuple: Trailing comma on bare tuple prohibited
   --> docs/development.md#block0.py:576:62
    |
574 | type(scope): brief description
575 |
576 | Detailed explanation of changes made, why they were necessary,
    |                                                              ^
577 | and any breaking changes introduced.
    |

invalid-syntax: Expected a statement
   --> docs/development.md#block0.py:577:1
    |
576 | Detailed explanation of changes made, why they were necessary,
577 | and any breaking changes introduced.
    | ^^^
578 |
579 | Fixes #123
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:577:9
    |
576 | Detailed explanation of changes made, why they were necessary,
577 | and any breaking changes introduced.
    |         ^^^^^^^^
578 |
579 | Fixes #123
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:577:18
    |
576 | Detailed explanation of changes made, why they were necessary,
577 | and any breaking changes introduced.
    |                  ^^^^^^^
578 |
579 | Fixes #123
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:577:26
    |
576 | Detailed explanation of changes made, why they were necessary,
577 | and any breaking changes introduced.
    |                          ^^^^^^^^^^
578 |
579 | Fixes #123
    |

invalid-syntax: Expected an identifier
   --> docs/development.md#block0.py:577:37
    |
576 | Detailed explanation of changes made, why they were necessary,
577 | and any breaking changes introduced.
    |                                     ^
578 |
579 | Fixes #123
    |

too-few-spaces-before-inline-comment: Insert at least two spaces before an inline comment
   --> docs/development.md#block0.py:579:6
    |
577 | and any breaking changes introduced.
578 |
579 | Fixes #123
    |      ^
580 | ```
581 | Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`
    |
help: Insert spaces

no-space-after-inline-comment: Inline comment should start with `# `
   --> docs/development.md#block0.py:579:7
    |
577 | and any breaking changes introduced.
578 |
579 | Fixes #123
    |       ^^^^
580 | ```
581 | Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`
    |
help: Format space

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:580:1
    |
579 | Fixes #123
580 | ```
    | ^
581 | Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:580:2
    |
579 | Fixes #123
580 | ```
    |  ^
581 | Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:580:3
    |
579 | Fixes #123
580 | ```
    |   ^
581 | Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`
    |

invalid-syntax: Expected a statement
   --> docs/development.md#block0.py:580:4
    |
579 | Fixes #123
580 | ```
    |    ^
581 | Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:581:8
    |
579 | Fixes #123
580 | ```
581 | Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`
    |        ^
582 |
583 | ### Review Process
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:581:13
    |
579 | Fixes #123
580 | ```
581 | Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`
    |             ^
582 |
583 | ### Review Process
    |

invalid-syntax: Expected a statement
   --> docs/development.md#block0.py:581:14
    |
579 | Fixes #123
580 | ```
581 | Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`
    |              ^
582 |
583 | ### Review Process
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:581:16
    |
579 | Fixes #123
580 | ```
581 | Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`
    |                ^
582 |
583 | ### Review Process
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:581:20
    |
579 | Fixes #123
580 | ```
581 | Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`
    |                    ^
582 |
583 | ### Review Process
    |

invalid-syntax: Expected a statement
   --> docs/development.md#block0.py:581:21
    |
579 | Fixes #123
580 | ```
581 | Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`
    |                     ^
582 |
583 | ### Review Process
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:581:23
    |
579 | Fixes #123
580 | ```
581 | Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`
    |                       ^
582 |
583 | ### Review Process
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:581:28
    |
579 | Fixes #123
580 | ```
581 | Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`
    |                            ^
582 |
583 | ### Review Process
    |

invalid-syntax: Expected a statement
   --> docs/development.md#block0.py:581:29
    |
579 | Fixes #123
580 | ```
581 | Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`
    |                             ^
582 |
583 | ### Review Process
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:581:31
    |
579 | Fixes #123
580 | ```
581 | Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`
    |                               ^
582 |
583 | ### Review Process
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:581:36
    |
579 | Fixes #123
580 | ```
581 | Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`
    |                                    ^
582 |
583 | ### Review Process
    |

invalid-syntax: Expected a statement
   --> docs/development.md#block0.py:581:37
    |
579 | Fixes #123
580 | ```
581 | Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`
    |                                     ^
582 |
583 | ### Review Process
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:581:39
    |
579 | Fixes #123
580 | ```
581 | Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`
    |                                       ^
582 |
583 | ### Review Process
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:581:48
    |
579 | Fixes #123
580 | ```
581 | Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`
    |                                                ^
582 |
583 | ### Review Process
    |

invalid-syntax: Expected a statement
   --> docs/development.md#block0.py:581:49
    |
579 | Fixes #123
580 | ```
581 | Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`
    |                                                 ^
582 |
583 | ### Review Process
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:581:51
    |
579 | Fixes #123
580 | ```
581 | Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`
    |                                                   ^
582 |
583 | ### Review Process
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:581:56
    |
579 | Fixes #123
580 | ```
581 | Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`
    |                                                        ^
582 |
583 | ### Review Process
    |

invalid-syntax: Expected a statement
   --> docs/development.md#block0.py:581:57
    |
579 | Fixes #123
580 | ```
581 | Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`
    |                                                         ^
582 |
583 | ### Review Process
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:581:59
    |
579 | Fixes #123
580 | ```
581 | Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`
    |                                                           ^
582 |
583 | ### Review Process
    |

invalid-syntax: Got unexpected token `
   --> docs/development.md#block0.py:581:65
    |
579 | Fixes #123
580 | ```
581 | Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`
    |                                                                 ^
582 |
583 | ### Review Process
    |

invalid-syntax: Expected a statement
   --> docs/development.md#block0.py:581:66
    |
579 | Fixes #123
580 | ```
581 | Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`
    |                                                                  ^
582 |
583 | ### Review Process
    |

multiple-leading-hashes-for-block-comment: Too many leading `#` before block comment
   --> docs/development.md#block0.py:583:1
    |
581 | Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`
582 |
583 | ### Review Process
    | ^^^^^^^^^^^^^^^^^^
584 |
585 | 1. **Automated Checks**: CI/CD pipeline runs quality gates
    |
help: Remove leading `#`

missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
   --> docs/development.md#block0.py:585:4
    |
583 | ### Review Process
584 |
585 | 1. **Automated Checks**: CI/CD pipeline runs quality gates
    |    ^^
586 | 1. **Architecture Review**: Ensure FLEXT pattern compliance
587 | 1. **Security Review**: Check for vulnerabilities
    |
help: Add missing whitespace

invalid-syntax: Invalid annotated assignment target
   --> docs/development.md#block0.py:585:16
    |
583 | ### Review Process
584 |
585 | 1. **Automated Checks**: CI/CD pipeline runs quality gates
    |                ^^^^^^^^
586 | 1. **Architecture Review**: Ensure FLEXT pattern compliance
587 | 1. **Security Review**: Check for vulnerabilities
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:585:16
    |
583 | ### Review Process
584 |
585 | 1. **Automated Checks**: CI/CD pipeline runs quality gates
    |                ^^^^^^
586 | 1. **Architecture Review**: Ensure FLEXT pattern compliance
587 | 1. **Security Review**: Check for vulnerabilities
    |

invalid-syntax: Expected an expression
   --> docs/development.md#block0.py:585:24
    |
583 | ### Review Process
584 |
585 | 1. **Automated Checks**: CI/CD pipeline runs quality gates
    |                        ^
586 | 1. **Architecture Review**: Ensure FLEXT pattern compliance
587 | 1. **Security Review**: Check for vulnerabilities
    |

missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
   --> docs/development.md#block0.py:585:28
    |
583 | ### Review Process
584 |
585 | 1. **Automated Checks**: CI/CD pipeline runs quality gates
    |                            ^
586 | 1. **Architecture Review**: Ensure FLEXT pattern compliance
587 | 1. **Security Review**: Check for vulnerabilities
    |
help: Add missing whitespace

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:585:32
    |
583 | ### Review Process
584 |
585 | 1. **Automated Checks**: CI/CD pipeline runs quality gates
    |                                ^^^^^^^^
586 | 1. **Architecture Review**: Ensure FLEXT pattern compliance
587 | 1. **Security Review**: Check for vulnerabilities
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:585:41
    |
583 | ### Review Process
584 |
585 | 1. **Automated Checks**: CI/CD pipeline runs quality gates
    |                                         ^^^^
586 | 1. **Architecture Review**: Ensure FLEXT pattern compliance
587 | 1. **Security Review**: Check for vulnerabilities
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:585:46
    |
583 | ### Review Process
584 |
585 | 1. **Automated Checks**: CI/CD pipeline runs quality gates
    |                                              ^^^^^^^
586 | 1. **Architecture Review**: Ensure FLEXT pattern compliance
587 | 1. **Security Review**: Check for vulnerabilities
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:585:54
    |
583 | ### Review Process
584 |
585 | 1. **Automated Checks**: CI/CD pipeline runs quality gates
    |                                                      ^^^^^
586 | 1. **Architecture Review**: Ensure FLEXT pattern compliance
587 | 1. **Security Review**: Check for vulnerabilities
    |

missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
   --> docs/development.md#block0.py:586:4
    |
585 | 1. **Automated Checks**: CI/CD pipeline runs quality gates
586 | 1. **Architecture Review**: Ensure FLEXT pattern compliance
    |    ^^
587 | 1. **Security Review**: Check for vulnerabilities
588 | 1. **Performance Review**: Validate no performance regressions
    |
help: Add missing whitespace

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:586:19
    |
585 | 1. **Automated Checks**: CI/CD pipeline runs quality gates
586 | 1. **Architecture Review**: Ensure FLEXT pattern compliance
    |                   ^^^^^^
587 | 1. **Security Review**: Check for vulnerabilities
588 | 1. **Performance Review**: Validate no performance regressions
    |

invalid-syntax: Invalid annotated assignment target
   --> docs/development.md#block0.py:586:19
    |
585 | 1. **Automated Checks**: CI/CD pipeline runs quality gates
586 | 1. **Architecture Review**: Ensure FLEXT pattern compliance
    |                   ^^^^^^^^
587 | 1. **Security Review**: Check for vulnerabilities
588 | 1. **Performance Review**: Validate no performance regressions
    |

invalid-syntax: Expected an expression
   --> docs/development.md#block0.py:586:27
    |
585 | 1. **Automated Checks**: CI/CD pipeline runs quality gates
586 | 1. **Architecture Review**: Ensure FLEXT pattern compliance
    |                           ^
587 | 1. **Security Review**: Check for vulnerabilities
588 | 1. **Performance Review**: Validate no performance regressions
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:586:36
    |
585 | 1. **Automated Checks**: CI/CD pipeline runs quality gates
586 | 1. **Architecture Review**: Ensure FLEXT pattern compliance
    |                                    ^^^^^
587 | 1. **Security Review**: Check for vulnerabilities
588 | 1. **Performance Review**: Validate no performance regressions
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:586:42
    |
585 | 1. **Automated Checks**: CI/CD pipeline runs quality gates
586 | 1. **Architecture Review**: Ensure FLEXT pattern compliance
    |                                          ^^^^^^^
587 | 1. **Security Review**: Check for vulnerabilities
588 | 1. **Performance Review**: Validate no performance regressions
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:586:50
    |
585 | 1. **Automated Checks**: CI/CD pipeline runs quality gates
586 | 1. **Architecture Review**: Ensure FLEXT pattern compliance
    |                                                  ^^^^^^^^^^
587 | 1. **Security Review**: Check for vulnerabilities
588 | 1. **Performance Review**: Validate no performance regressions
    |

missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
   --> docs/development.md#block0.py:587:4
    |
585 | 1. **Automated Checks**: CI/CD pipeline runs quality gates
586 | 1. **Architecture Review**: Ensure FLEXT pattern compliance
587 | 1. **Security Review**: Check for vulnerabilities
    |    ^^
588 | 1. **Performance Review**: Validate no performance regressions
589 | 1. **Documentation Review**: Ensure documentation is updated
    |
help: Add missing whitespace

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:587:15
    |
585 | 1. **Automated Checks**: CI/CD pipeline runs quality gates
586 | 1. **Architecture Review**: Ensure FLEXT pattern compliance
587 | 1. **Security Review**: Check for vulnerabilities
    |               ^^^^^^
588 | 1. **Performance Review**: Validate no performance regressions
589 | 1. **Documentation Review**: Ensure documentation is updated
    |

invalid-syntax: Invalid annotated assignment target
   --> docs/development.md#block0.py:587:15
    |
585 | 1. **Automated Checks**: CI/CD pipeline runs quality gates
586 | 1. **Architecture Review**: Ensure FLEXT pattern compliance
587 | 1. **Security Review**: Check for vulnerabilities
    |               ^^^^^^^^
588 | 1. **Performance Review**: Validate no performance regressions
589 | 1. **Documentation Review**: Ensure documentation is updated
    |

invalid-syntax: Expected an expression
   --> docs/development.md#block0.py:587:23
    |
585 | 1. **Automated Checks**: CI/CD pipeline runs quality gates
586 | 1. **Architecture Review**: Ensure FLEXT pattern compliance
587 | 1. **Security Review**: Check for vulnerabilities
    |                       ^
588 | 1. **Performance Review**: Validate no performance regressions
589 | 1. **Documentation Review**: Ensure documentation is updated
    |

invalid-syntax: Compound statements are not allowed on the same line as simple statements
   --> docs/development.md#block0.py:587:31
    |
585 | 1. **Automated Checks**: CI/CD pipeline runs quality gates
586 | 1. **Architecture Review**: Ensure FLEXT pattern compliance
587 | 1. **Security Review**: Check for vulnerabilities
    |                               ^^^
588 | 1. **Performance Review**: Validate no performance regressions
589 | 1. **Documentation Review**: Ensure documentation is updated
    |

invalid-syntax: Expected `in`, found newline
   --> docs/development.md#block0.py:587:50
    |
585 | 1. **Automated Checks**: CI/CD pipeline runs quality gates
586 | 1. **Architecture Review**: Ensure FLEXT pattern compliance
587 | 1. **Security Review**: Check for vulnerabilities
    |                                                  ^
588 | 1. **Performance Review**: Validate no performance regressions
589 | 1. **Documentation Review**: Ensure documentation is updated
    |

invalid-syntax: Expected an indented block after `for` statement
   --> docs/development.md#block0.py:588:1
    |
586 | 1. **Architecture Review**: Ensure FLEXT pattern compliance
587 | 1. **Security Review**: Check for vulnerabilities
588 | 1. **Performance Review**: Validate no performance regressions
    | ^^
589 | 1. **Documentation Review**: Ensure documentation is updated
    |

missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
   --> docs/development.md#block0.py:588:4
    |
586 | 1. **Architecture Review**: Ensure FLEXT pattern compliance
587 | 1. **Security Review**: Check for vulnerabilities
588 | 1. **Performance Review**: Validate no performance regressions
    |    ^^
589 | 1. **Documentation Review**: Ensure documentation is updated
    |
help: Add missing whitespace

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:588:18
    |
586 | 1. **Architecture Review**: Ensure FLEXT pattern compliance
587 | 1. **Security Review**: Check for vulnerabilities
588 | 1. **Performance Review**: Validate no performance regressions
    |                  ^^^^^^
589 | 1. **Documentation Review**: Ensure documentation is updated
    |

invalid-syntax: Invalid annotated assignment target
   --> docs/development.md#block0.py:588:18
    |
586 | 1. **Architecture Review**: Ensure FLEXT pattern compliance
587 | 1. **Security Review**: Check for vulnerabilities
588 | 1. **Performance Review**: Validate no performance regressions
    |                  ^^^^^^^^
589 | 1. **Documentation Review**: Ensure documentation is updated
    |

invalid-syntax: Expected an expression
   --> docs/development.md#block0.py:588:26
    |
586 | 1. **Architecture Review**: Ensure FLEXT pattern compliance
587 | 1. **Security Review**: Check for vulnerabilities
588 | 1. **Performance Review**: Validate no performance regressions
    |                          ^
589 | 1. **Documentation Review**: Ensure documentation is updated
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:588:37
    |
586 | 1. **Architecture Review**: Ensure FLEXT pattern compliance
587 | 1. **Security Review**: Check for vulnerabilities
588 | 1. **Performance Review**: Validate no performance regressions
    |                                     ^^
589 | 1. **Documentation Review**: Ensure documentation is updated
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:588:40
    |
586 | 1. **Architecture Review**: Ensure FLEXT pattern compliance
587 | 1. **Security Review**: Check for vulnerabilities
588 | 1. **Performance Review**: Validate no performance regressions
    |                                        ^^^^^^^^^^^
589 | 1. **Documentation Review**: Ensure documentation is updated
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:588:52
    |
586 | 1. **Architecture Review**: Ensure FLEXT pattern compliance
587 | 1. **Security Review**: Check for vulnerabilities
588 | 1. **Performance Review**: Validate no performance regressions
    |                                                    ^^^^^^^^^^^
589 | 1. **Documentation Review**: Ensure documentation is updated
    |

missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
   --> docs/development.md#block0.py:589:4
    |
587 | 1. **Security Review**: Check for vulnerabilities
588 | 1. **Performance Review**: Validate no performance regressions
589 | 1. **Documentation Review**: Ensure documentation is updated
    |    ^^
590 |
591 | ______________________________________________________________________
    |
help: Add missing whitespace

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:589:20
    |
587 | 1. **Security Review**: Check for vulnerabilities
588 | 1. **Performance Review**: Validate no performance regressions
589 | 1. **Documentation Review**: Ensure documentation is updated
    |                    ^^^^^^
590 |
591 | ______________________________________________________________________
    |

invalid-syntax: Invalid annotated assignment target
   --> docs/development.md#block0.py:589:20
    |
587 | 1. **Security Review**: Check for vulnerabilities
588 | 1. **Performance Review**: Validate no performance regressions
589 | 1. **Documentation Review**: Ensure documentation is updated
    |                    ^^^^^^^^
590 |
591 | ______________________________________________________________________
    |

invalid-syntax: Expected an expression
   --> docs/development.md#block0.py:589:28
    |
587 | 1. **Security Review**: Check for vulnerabilities
588 | 1. **Performance Review**: Validate no performance regressions
589 | 1. **Documentation Review**: Ensure documentation is updated
    |                            ^
590 |
591 | ______________________________________________________________________
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:589:37
    |
587 | 1. **Security Review**: Check for vulnerabilities
588 | 1. **Performance Review**: Validate no performance regressions
589 | 1. **Documentation Review**: Ensure documentation is updated
    |                                     ^^^^^^^^^^^^^
590 |
591 | ______________________________________________________________________
    |

invalid-syntax: Expected an expression
   --> docs/development.md#block0.py:593:1
    |
591 | ______________________________________________________________________
592 |
593 | **Document Version**: 1.0\
    | ^^
594 | **Last Updated**: 2025-08-04\
595 | **Next Review**: 2025-08-11
    |

invalid-syntax: Invalid annotated assignment target
   --> docs/development.md#block0.py:593:12
    |
591 | ______________________________________________________________________
592 |
593 | **Document Version**: 1.0\
    |            ^^^^^^^^^
594 | **Last Updated**: 2025-08-04\
595 | **Next Review**: 2025-08-11
    |

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:593:12
    |
591 | ______________________________________________________________________
592 |
593 | **Document Version**: 1.0\
    |            ^^^^^^^
594 | **Last Updated**: 2025-08-04\
595 | **Next Review**: 2025-08-11
    |

invalid-syntax: Expected an expression
   --> docs/development.md#block0.py:593:21
    |
591 | ______________________________________________________________________
592 |
593 | **Document Version**: 1.0\
    |                     ^
594 | **Last Updated**: 2025-08-04\
595 | **Next Review**: 2025-08-11
    |

missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
   --> docs/development.md#block0.py:594:1
    |
593 | **Document Version**: 1.0\
594 | **Last Updated**: 2025-08-04\
    | ^^
595 | **Next Review**: 2025-08-11
    |
help: Add missing whitespace

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:594:8
    |
593 | **Document Version**: 1.0\
594 | **Last Updated**: 2025-08-04\
    |        ^^^^^^^
595 | **Next Review**: 2025-08-11
    |

invalid-syntax: Invalid annotated assignment target
   --> docs/development.md#block0.py:594:8
    |
593 | **Document Version**: 1.0\
594 | **Last Updated**: 2025-08-04\
    |        ^^^^^^^^^
595 | **Next Review**: 2025-08-11
    |

invalid-syntax: Expected an expression
   --> docs/development.md#block0.py:594:17
    |
593 | **Document Version**: 1.0\
594 | **Last Updated**: 2025-08-04\
    |                 ^
595 | **Next Review**: 2025-08-11
    |

missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
   --> docs/development.md#block0.py:594:23
    |
593 | **Document Version**: 1.0\
594 | **Last Updated**: 2025-08-04\
    |                       ^
595 | **Next Review**: 2025-08-11
    |
help: Add missing whitespace

invalid-syntax: Invalid decimal integer literal
   --> docs/development.md#block0.py:594:24
    |
593 | **Document Version**: 1.0\
594 | **Last Updated**: 2025-08-04\
    |                        ^^
595 | **Next Review**: 2025-08-11
    |

missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
   --> docs/development.md#block0.py:594:26
    |
593 | **Document Version**: 1.0\
594 | **Last Updated**: 2025-08-04\
    |                          ^
595 | **Next Review**: 2025-08-11
    |
help: Add missing whitespace

invalid-syntax: Invalid decimal integer literal
   --> docs/development.md#block0.py:594:27
    |
593 | **Document Version**: 1.0\
594 | **Last Updated**: 2025-08-04\
    |                           ^^
595 | **Next Review**: 2025-08-11
    |

invalid-syntax: Expected an expression
   --> docs/development.md#block0.py:595:1
    |
593 | **Document Version**: 1.0\
594 | **Last Updated**: 2025-08-04\
595 | **Next Review**: 2025-08-11
    | ^^

missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
   --> docs/development.md#block0.py:595:1
    |
593 | **Document Version**: 1.0\
594 | **Last Updated**: 2025-08-04\
595 | **Next Review**: 2025-08-11
    | ^^
help: Add missing whitespace

invalid-syntax: Invalid annotated assignment target
   --> docs/development.md#block0.py:595:8
    |
593 | **Document Version**: 1.0\
594 | **Last Updated**: 2025-08-04\
595 | **Next Review**: 2025-08-11
    |        ^^^^^^^^

invalid-syntax: Simple statements must be separated by newlines or semicolons
   --> docs/development.md#block0.py:595:8
    |
593 | **Document Version**: 1.0\
594 | **Last Updated**: 2025-08-04\
595 | **Next Review**: 2025-08-11
    |        ^^^^^^

invalid-syntax: Expected an expression
   --> docs/development.md#block0.py:595:16
    |
593 | **Document Version**: 1.0\
594 | **Last Updated**: 2025-08-04\
595 | **Next Review**: 2025-08-11
    |                ^

missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
   --> docs/development.md#block0.py:595:22
    |
593 | **Document Version**: 1.0\
594 | **Last Updated**: 2025-08-04\
595 | **Next Review**: 2025-08-11
    |                      ^
help: Add missing whitespace

invalid-syntax: Invalid decimal integer literal
   --> docs/development.md#block0.py:595:23
    |
593 | **Document Version**: 1.0\
594 | **Last Updated**: 2025-08-04\
595 | **Next Review**: 2025-08-11
    |                       ^^

missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
   --> docs/development.md#block0.py:595:25
    |
593 | **Document Version**: 1.0\
594 | **Last Updated**: 2025-08-04\
595 | **Next Review**: 2025-08-11
    |                         ^
help: Add missing whitespace

Found 361 errors. |
| docs/guides/python-module-organization.md | python_codeblock | medium | block #0: missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
 --> docs/guides/python-module-organization.md#block0.py:1:4
  |
1 | src/flext_target_oracle/
  |    ^
2 | ├── __init__.py              # 🎯 Public API gateway & exports
3 | ├── settings.py                # ⚙️ m.Value configuration patterns
  |
help: Add missing whitespace

missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
 --> docs/guides/python-module-organization.md#block0.py:1:24
  |
1 | src/flext_target_oracle/
  |                        ^
2 | ├── __init__.py              # 🎯 Public API gateway & exports
3 | ├── settings.py                # ⚙️ m.Value configuration patterns
  |
help: Add missing whitespace

invalid-syntax: Expected an expression
 --> docs/guides/python-module-organization.md#block0.py:1:25
  |
1 | src/flext_target_oracle/
  |                         ^
2 | ├── __init__.py              # 🎯 Public API gateway & exports
3 | ├── settings.py                # ⚙️ m.Value configuration patterns
  |

invalid-syntax: Got unexpected token ├
 --> docs/guides/python-module-organization.md#block0.py:2:1
  |
1 | src/flext_target_oracle/
2 | ├── __init__.py              # 🎯 Public API gateway & exports
  | ^
3 | ├── settings.py                # ⚙️ m.Value configuration patterns
4 | ├── target.py                # 🎯 Singer Target implementation
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block0.py:2:2
  |
1 | src/flext_target_oracle/
2 | ├── __init__.py              # 🎯 Public API gateway & exports
  |  ^
3 | ├── settings.py                # ⚙️ m.Value configuration patterns
4 | ├── target.py                # 🎯 Singer Target implementation
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block0.py:2:3
  |
1 | src/flext_target_oracle/
2 | ├── __init__.py              # 🎯 Public API gateway & exports
  |   ^
3 | ├── settings.py                # ⚙️ m.Value configuration patterns
4 | ├── target.py                # 🎯 Singer Target implementation
  |

invalid-syntax: Got unexpected token ├
 --> docs/guides/python-module-organization.md#block0.py:3:1
  |
1 | src/flext_target_oracle/
2 | ├── __init__.py              # 🎯 Public API gateway & exports
3 | ├── settings.py                # ⚙️ m.Value configuration patterns
  | ^
4 | ├── target.py                # 🎯 Singer Target implementation
5 | ├── loader.py                # 🔧 Oracle data loading operations
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block0.py:3:2
  |
1 | src/flext_target_oracle/
2 | ├── __init__.py              # 🎯 Public API gateway & exports
3 | ├── settings.py                # ⚙️ m.Value configuration patterns
  |  ^
4 | ├── target.py                # 🎯 Singer Target implementation
5 | ├── loader.py                # 🔧 Oracle data loading operations
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block0.py:3:3
  |
1 | src/flext_target_oracle/
2 | ├── __init__.py              # 🎯 Public API gateway & exports
3 | ├── settings.py                # ⚙️ m.Value configuration patterns
  |   ^
4 | ├── target.py                # 🎯 Singer Target implementation
5 | ├── loader.py                # 🔧 Oracle data loading operations
  |

invalid-syntax: Got unexpected token ├
 --> docs/guides/python-module-organization.md#block0.py:4:1
  |
2 | ├── __init__.py              # 🎯 Public API gateway & exports
3 | ├── settings.py                # ⚙️ m.Value configuration patterns
4 | ├── target.py                # 🎯 Singer Target implementation
  | ^
5 | ├── loader.py                # 🔧 Oracle data loading operations
6 | └── exceptions.py            # 🚨 Domain-specific error hierarchy
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block0.py:4:2
  |
2 | ├── __init__.py              # 🎯 Public API gateway & exports
3 | ├── settings.py                # ⚙️ m.Value configuration patterns
4 | ├── target.py                # 🎯 Singer Target implementation
  |  ^
5 | ├── loader.py                # 🔧 Oracle data loading operations
6 | └── exceptions.py            # 🚨 Domain-specific error hierarchy
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block0.py:4:3
  |
2 | ├── __init__.py              # 🎯 Public API gateway & exports
3 | ├── settings.py                # ⚙️ m.Value configuration patterns
4 | ├── target.py                # 🎯 Singer Target implementation
  |   ^
5 | ├── loader.py                # 🔧 Oracle data loading operations
6 | └── exceptions.py            # 🚨 Domain-specific error hierarchy
  |

invalid-syntax: Got unexpected token ├
 --> docs/guides/python-module-organization.md#block0.py:5:1
  |
3 | ├── settings.py                # ⚙️ m.Value configuration patterns
4 | ├── target.py                # 🎯 Singer Target implementation
5 | ├── loader.py                # 🔧 Oracle data loading operations
  | ^
6 | └── exceptions.py            # 🚨 Domain-specific error hierarchy
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block0.py:5:2
  |
3 | ├── settings.py                # ⚙️ m.Value configuration patterns
4 | ├── target.py                # 🎯 Singer Target implementation
5 | ├── loader.py                # 🔧 Oracle data loading operations
  |  ^
6 | └── exceptions.py            # 🚨 Domain-specific error hierarchy
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block0.py:5:3
  |
3 | ├── settings.py                # ⚙️ m.Value configuration patterns
4 | ├── target.py                # 🎯 Singer Target implementation
5 | ├── loader.py                # 🔧 Oracle data loading operations
  |   ^
6 | └── exceptions.py            # 🚨 Domain-specific error hierarchy
  |

invalid-syntax: Got unexpected token └
 --> docs/guides/python-module-organization.md#block0.py:6:1
  |
4 | ├── target.py                # 🎯 Singer Target implementation
5 | ├── loader.py                # 🔧 Oracle data loading operations
6 | └── exceptions.py            # 🚨 Domain-specific error hierarchy
  | ^

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block0.py:6:2
  |
4 | ├── target.py                # 🎯 Singer Target implementation
5 | ├── loader.py                # 🔧 Oracle data loading operations
6 | └── exceptions.py            # 🚨 Domain-specific error hierarchy
  |  ^

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block0.py:6:3
  |
4 | ├── target.py                # 🎯 Singer Target implementation
5 | ├── loader.py                # 🔧 Oracle data loading operations
6 | └── exceptions.py            # 🚨 Domain-specific error hierarchy
  |   ^

Found 18 errors. |
| docs/guides/python-module-organization.md | python_codeblock | medium | block #1: invalid-syntax: Expected `,`, found `.`
  --> docs/guides/python-module-organization.md#block1.py:15:23
   |
13 | from flext_cli import u
14 | from flext_core import FlextSettings
15 | from pydantic import u.Field, m.field_validator
   |                       ^
16 | from enum import StrEnum, unique
   |

invalid-syntax: Expected `,`, found `.`
  --> docs/guides/python-module-organization.md#block1.py:15:32
   |
13 | from flext_cli import u
14 | from flext_core import FlextSettings
15 | from pydantic import u.Field, m.field_validator
   |                                ^
16 | from enum import StrEnum, unique
   |

Found 2 errors. |
| docs/guides/python-module-organization.md | python_codeblock | medium | block #2: missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
 --> docs/guides/python-module-organization.md#block2.py:1:4
  |
1 | src/flext_target_oracle/
  |    ^
2 | ├── __init__.py              # 🎯 Clean public API exports
3 | ├── settings/                  # ⚙️ Configuration module
  |
help: Add missing whitespace

missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
 --> docs/guides/python-module-organization.md#block2.py:1:24
  |
1 | src/flext_target_oracle/
  |                        ^
2 | ├── __init__.py              # 🎯 Clean public API exports
3 | ├── settings/                  # ⚙️ Configuration module
  |
help: Add missing whitespace

invalid-syntax: Expected an expression
 --> docs/guides/python-module-organization.md#block2.py:1:25
  |
1 | src/flext_target_oracle/
  |                         ^
2 | ├── __init__.py              # 🎯 Clean public API exports
3 | ├── settings/                  # ⚙️ Configuration module
  |

invalid-syntax: Got unexpected token ├
 --> docs/guides/python-module-organization.md#block2.py:2:1
  |
1 | src/flext_target_oracle/
2 | ├── __init__.py              # 🎯 Clean public API exports
  | ^
3 | ├── settings/                  # ⚙️ Configuration module
4 | │   ├── __init__.py         # Configuration exports
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block2.py:2:2
  |
1 | src/flext_target_oracle/
2 | ├── __init__.py              # 🎯 Clean public API exports
  |  ^
3 | ├── settings/                  # ⚙️ Configuration module
4 | │   ├── __init__.py         # Configuration exports
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block2.py:2:3
  |
1 | src/flext_target_oracle/
2 | ├── __init__.py              # 🎯 Clean public API exports
  |   ^
3 | ├── settings/                  # ⚙️ Configuration module
4 | │   ├── __init__.py         # Configuration exports
  |

invalid-syntax: Got unexpected token ├
 --> docs/guides/python-module-organization.md#block2.py:3:1
  |
1 | src/flext_target_oracle/
2 | ├── __init__.py              # 🎯 Clean public API exports
3 | ├── settings/                  # ⚙️ Configuration module
  | ^
4 | │   ├── __init__.py         # Configuration exports
5 | │   ├── settings.py         # FlextOracleTargetSettings
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block2.py:3:2
  |
1 | src/flext_target_oracle/
2 | ├── __init__.py              # 🎯 Clean public API exports
3 | ├── settings/                  # ⚙️ Configuration module
  |  ^
4 | │   ├── __init__.py         # Configuration exports
5 | │   ├── settings.py         # FlextOracleTargetSettings
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block2.py:3:3
  |
1 | src/flext_target_oracle/
2 | ├── __init__.py              # 🎯 Clean public API exports
3 | ├── settings/                  # ⚙️ Configuration module
  |   ^
4 | │   ├── __init__.py         # Configuration exports
5 | │   ├── settings.py         # FlextOracleTargetSettings
  |

missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
 --> docs/guides/python-module-organization.md#block2.py:3:13
  |
1 | src/flext_target_oracle/
2 | ├── __init__.py              # 🎯 Clean public API exports
3 | ├── settings/                  # ⚙️ Configuration module
  |             ^
4 | │   ├── __init__.py         # Configuration exports
5 | │   ├── settings.py         # FlextOracleTargetSettings
  |
help: Add missing whitespace

invalid-syntax: Expected an expression
 --> docs/guides/python-module-organization.md#block2.py:3:57
  |
1 | src/flext_target_oracle/
2 | ├── __init__.py              # 🎯 Clean public API exports
3 | ├── settings/                  # ⚙️ Configuration module
  |                                                        ^
4 | │   ├── __init__.py         # Configuration exports
5 | │   ├── settings.py         # FlextOracleTargetSettings
  |

invalid-syntax: Got unexpected token │
 --> docs/guides/python-module-organization.md#block2.py:4:1
  |
2 | ├── __init__.py              # 🎯 Clean public API exports
3 | ├── settings/                  # ⚙️ Configuration module
4 | │   ├── __init__.py         # Configuration exports
  | ^
5 | │   ├── settings.py         # FlextOracleTargetSettings
6 | │   ├── validation.py       # Domain validation rules
  |

invalid-syntax: Got unexpected token ├
 --> docs/guides/python-module-organization.md#block2.py:4:5
  |
2 | ├── __init__.py              # 🎯 Clean public API exports
3 | ├── settings/                  # ⚙️ Configuration module
4 | │   ├── __init__.py         # Configuration exports
  |     ^
5 | │   ├── settings.py         # FlextOracleTargetSettings
6 | │   ├── validation.py       # Domain validation rules
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block2.py:4:6
  |
2 | ├── __init__.py              # 🎯 Clean public API exports
3 | ├── settings/                  # ⚙️ Configuration module
4 | │   ├── __init__.py         # Configuration exports
  |      ^
5 | │   ├── settings.py         # FlextOracleTargetSettings
6 | │   ├── validation.py       # Domain validation rules
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block2.py:4:7
  |
2 | ├── __init__.py              # 🎯 Clean public API exports
3 | ├── settings/                  # ⚙️ Configuration module
4 | │   ├── __init__.py         # Configuration exports
  |       ^
5 | │   ├── settings.py         # FlextOracleTargetSettings
6 | │   ├── validation.py       # Domain validation rules
  |

invalid-syntax: Got unexpected token │
 --> docs/guides/python-module-organization.md#block2.py:5:1
  |
3 | ├── settings/                  # ⚙️ Configuration module
4 | │   ├── __init__.py         # Configuration exports
5 | │   ├── settings.py         # FlextOracleTargetSettings
  | ^
6 | │   ├── validation.py       # Domain validation rules
7 | │   └── constants.py        # Oracle-specific constants
  |

invalid-syntax: Got unexpected token ├
 --> docs/guides/python-module-organization.md#block2.py:5:5
  |
3 | ├── settings/                  # ⚙️ Configuration module
4 | │   ├── __init__.py         # Configuration exports
5 | │   ├── settings.py         # FlextOracleTargetSettings
  |     ^
6 | │   ├── validation.py       # Domain validation rules
7 | │   └── constants.py        # Oracle-specific constants
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block2.py:5:6
  |
3 | ├── settings/                  # ⚙️ Configuration module
4 | │   ├── __init__.py         # Configuration exports
5 | │   ├── settings.py         # FlextOracleTargetSettings
  |      ^
6 | │   ├── validation.py       # Domain validation rules
7 | │   └── constants.py        # Oracle-specific constants
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block2.py:5:7
  |
3 | ├── settings/                  # ⚙️ Configuration module
4 | │   ├── __init__.py         # Configuration exports
5 | │   ├── settings.py         # FlextOracleTargetSettings
  |       ^
6 | │   ├── validation.py       # Domain validation rules
7 | │   └── constants.py        # Oracle-specific constants
  |

invalid-syntax: Got unexpected token │
 --> docs/guides/python-module-organization.md#block2.py:6:1
  |
4 | │   ├── __init__.py         # Configuration exports
5 | │   ├── settings.py         # FlextOracleTargetSettings
6 | │   ├── validation.py       # Domain validation rules
  | ^
7 | │   └── constants.py        # Oracle-specific constants
8 | ├── domain/                  # 🏛️ Domain layer (if needed for complex targets)
  |

invalid-syntax: Got unexpected token ├
 --> docs/guides/python-module-organization.md#block2.py:6:5
  |
4 | │   ├── __init__.py         # Configuration exports
5 | │   ├── settings.py         # FlextOracleTargetSettings
6 | │   ├── validation.py       # Domain validation rules
  |     ^
7 | │   └── constants.py        # Oracle-specific constants
8 | ├── domain/                  # 🏛️ Domain layer (if needed for complex targets)
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block2.py:6:6
  |
4 | │   ├── __init__.py         # Configuration exports
5 | │   ├── settings.py         # FlextOracleTargetSettings
6 | │   ├── validation.py       # Domain validation rules
  |      ^
7 | │   └── constants.py        # Oracle-specific constants
8 | ├── domain/                  # 🏛️ Domain layer (if needed for complex targets)
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block2.py:6:7
  |
4 | │   ├── __init__.py         # Configuration exports
5 | │   ├── settings.py         # FlextOracleTargetSettings
6 | │   ├── validation.py       # Domain validation rules
  |       ^
7 | │   └── constants.py        # Oracle-specific constants
8 | ├── domain/                  # 🏛️ Domain layer (if needed for complex targets)
  |

invalid-syntax: Got unexpected token │
 --> docs/guides/python-module-organization.md#block2.py:7:1
  |
5 | │   ├── settings.py         # FlextOracleTargetSettings
6 | │   ├── validation.py       # Domain validation rules
7 | │   └── constants.py        # Oracle-specific constants
  | ^
8 | ├── domain/                  # 🏛️ Domain layer (if needed for complex targets)
9 | │   ├── __init__.py
  |

invalid-syntax: Got unexpected token └
 --> docs/guides/python-module-organization.md#block2.py:7:5
  |
5 | │   ├── settings.py         # FlextOracleTargetSettings
6 | │   ├── validation.py       # Domain validation rules
7 | │   └── constants.py        # Oracle-specific constants
  |     ^
8 | ├── domain/                  # 🏛️ Domain layer (if needed for complex targets)
9 | │   ├── __init__.py
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block2.py:7:6
  |
5 | │   ├── settings.py         # FlextOracleTargetSettings
6 | │   ├── validation.py       # Domain validation rules
7 | │   └── constants.py        # Oracle-specific constants
  |      ^
8 | ├── domain/                  # 🏛️ Domain layer (if needed for complex targets)
9 | │   ├── __init__.py
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block2.py:7:7
  |
5 | │   ├── settings.py         # FlextOracleTargetSettings
6 | │   ├── validation.py       # Domain validation rules
7 | │   └── constants.py        # Oracle-specific constants
  |       ^
8 | ├── domain/                  # 🏛️ Domain layer (if needed for complex targets)
9 | │   ├── __init__.py
  |

invalid-syntax: Got unexpected token ├
  --> docs/guides/python-module-organization.md#block2.py:8:1
   |
 6 | │   ├── validation.py       # Domain validation rules
 7 | │   └── constants.py        # Oracle-specific constants
 8 | ├── domain/                  # 🏛️ Domain layer (if needed for complex targets)
   | ^
 9 | │   ├── __init__.py
10 | │   ├── entities.py         # Domain entities (streams, records)
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block2.py:8:2
   |
 6 | │   ├── validation.py       # Domain validation rules
 7 | │   └── constants.py        # Oracle-specific constants
 8 | ├── domain/                  # 🏛️ Domain layer (if needed for complex targets)
   |  ^
 9 | │   ├── __init__.py
10 | │   ├── entities.py         # Domain entities (streams, records)
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block2.py:8:3
   |
 6 | │   ├── validation.py       # Domain validation rules
 7 | │   └── constants.py        # Oracle-specific constants
 8 | ├── domain/                  # 🏛️ Domain layer (if needed for complex targets)
   |   ^
 9 | │   ├── __init__.py
10 | │   ├── entities.py         # Domain entities (streams, records)
   |

missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
  --> docs/guides/python-module-organization.md#block2.py:8:11
   |
 6 | │   ├── validation.py       # Domain validation rules
 7 | │   └── constants.py        # Oracle-specific constants
 8 | ├── domain/                  # 🏛️ Domain layer (if needed for complex targets)
   |           ^
 9 | │   ├── __init__.py
10 | │   ├── entities.py         # Domain entities (streams, records)
   |
help: Add missing whitespace

invalid-syntax: Expected an expression
  --> docs/guides/python-module-organization.md#block2.py:8:79
   |
 6 | │   ├── validation.py       # Domain validation rules
 7 | │   └── constants.py        # Oracle-specific constants
 8 | ├── domain/                  # 🏛️ Domain layer (if needed for complex targets)
   |                                                                              ^
 9 | │   ├── __init__.py
10 | │   ├── entities.py         # Domain entities (streams, records)
   |

invalid-syntax: Got unexpected token │
  --> docs/guides/python-module-organization.md#block2.py:9:1
   |
 7 | │   └── constants.py        # Oracle-specific constants
 8 | ├── domain/                  # 🏛️ Domain layer (if needed for complex targets)
 9 | │   ├── __init__.py
   | ^
10 | │   ├── entities.py         # Domain entities (streams, records)
11 | │   └── value_objects.py    # Domain value objects (table names, schemas)
   |

invalid-syntax: Got unexpected token ├
  --> docs/guides/python-module-organization.md#block2.py:9:5
   |
 7 | │   └── constants.py        # Oracle-specific constants
 8 | ├── domain/                  # 🏛️ Domain layer (if needed for complex targets)
 9 | │   ├── __init__.py
   |     ^
10 | │   ├── entities.py         # Domain entities (streams, records)
11 | │   └── value_objects.py    # Domain value objects (table names, schemas)
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block2.py:9:6
   |
 7 | │   └── constants.py        # Oracle-specific constants
 8 | ├── domain/                  # 🏛️ Domain layer (if needed for complex targets)
 9 | │   ├── __init__.py
   |      ^
10 | │   ├── entities.py         # Domain entities (streams, records)
11 | │   └── value_objects.py    # Domain value objects (table names, schemas)
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block2.py:9:7
   |
 7 | │   └── constants.py        # Oracle-specific constants
 8 | ├── domain/                  # 🏛️ Domain layer (if needed for complex targets)
 9 | │   ├── __init__.py
   |       ^
10 | │   ├── entities.py         # Domain entities (streams, records)
11 | │   └── value_objects.py    # Domain value objects (table names, schemas)
   |

invalid-syntax: Got unexpected token │
  --> docs/guides/python-module-organization.md#block2.py:10:1
   |
 8 | ├── domain/                  # 🏛️ Domain layer (if needed for complex targets)
 9 | │   ├── __init__.py
10 | │   ├── entities.py         # Domain entities (streams, records)
   | ^
11 | │   └── value_objects.py    # Domain value objects (table names, schemas)
12 | ├── application/             # 📤 Application services
   |

invalid-syntax: Got unexpected token ├
  --> docs/guides/python-module-organization.md#block2.py:10:5
   |
 8 | ├── domain/                  # 🏛️ Domain layer (if needed for complex targets)
 9 | │   ├── __init__.py
10 | │   ├── entities.py         # Domain entities (streams, records)
   |     ^
11 | │   └── value_objects.py    # Domain value objects (table names, schemas)
12 | ├── application/             # 📤 Application services
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block2.py:10:6
   |
 8 | ├── domain/                  # 🏛️ Domain layer (if needed for complex targets)
 9 | │   ├── __init__.py
10 | │   ├── entities.py         # Domain entities (streams, records)
   |      ^
11 | │   └── value_objects.py    # Domain value objects (table names, schemas)
12 | ├── application/             # 📤 Application services
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block2.py:10:7
   |
 8 | ├── domain/                  # 🏛️ Domain layer (if needed for complex targets)
 9 | │   ├── __init__.py
10 | │   ├── entities.py         # Domain entities (streams, records)
   |       ^
11 | │   └── value_objects.py    # Domain value objects (table names, schemas)
12 | ├── application/             # 📤 Application services
   |

invalid-syntax: Got unexpected token │
  --> docs/guides/python-module-organization.md#block2.py:11:1
   |
 9 | │   ├── __init__.py
10 | │   ├── entities.py         # Domain entities (streams, records)
11 | │   └── value_objects.py    # Domain value objects (table names, schemas)
   | ^
12 | ├── application/             # 📤 Application services
13 | │   ├── __init__.py
   |

invalid-syntax: Got unexpected token └
  --> docs/guides/python-module-organization.md#block2.py:11:5
   |
 9 | │   ├── __init__.py
10 | │   ├── entities.py         # Domain entities (streams, records)
11 | │   └── value_objects.py    # Domain value objects (table names, schemas)
   |     ^
12 | ├── application/             # 📤 Application services
13 | │   ├── __init__.py
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block2.py:11:6
   |
 9 | │   ├── __init__.py
10 | │   ├── entities.py         # Domain entities (streams, records)
11 | │   └── value_objects.py    # Domain value objects (table names, schemas)
   |      ^
12 | ├── application/             # 📤 Application services
13 | │   ├── __init__.py
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block2.py:11:7
   |
 9 | │   ├── __init__.py
10 | │   ├── entities.py         # Domain entities (streams, records)
11 | │   └── value_objects.py    # Domain value objects (table names, schemas)
   |       ^
12 | ├── application/             # 📤 Application services
13 | │   ├── __init__.py
   |

invalid-syntax: Got unexpected token ├
  --> docs/guides/python-module-organization.md#block2.py:12:1
   |
10 | │   ├── entities.py         # Domain entities (streams, records)
11 | │   └── value_objects.py    # Domain value objects (table names, schemas)
12 | ├── application/             # 📤 Application services
   | ^
13 | │   ├── __init__.py
14 | │   ├── target.py           # Main Singer Target implementation
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block2.py:12:2
   |
10 | │   ├── entities.py         # Domain entities (streams, records)
11 | │   └── value_objects.py    # Domain value objects (table names, schemas)
12 | ├── application/             # 📤 Application services
   |  ^
13 | │   ├── __init__.py
14 | │   ├── target.py           # Main Singer Target implementation
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block2.py:12:3
   |
10 | │   ├── entities.py         # Domain entities (streams, records)
11 | │   └── value_objects.py    # Domain value objects (table names, schemas)
12 | ├── application/             # 📤 Application services
   |   ^
13 | │   ├── __init__.py
14 | │   ├── target.py           # Main Singer Target implementation
   |

missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
  --> docs/guides/python-module-organization.md#block2.py:12:16
   |
10 | │   ├── entities.py         # Domain entities (streams, records)
11 | │   └── value_objects.py    # Domain value objects (table names, schemas)
12 | ├── application/             # 📤 Application services
   |                ^
13 | │   ├── __init__.py
14 | │   ├── target.py           # Main Singer Target implementation
   |
help: Add missing whitespace

invalid-syntax: Expected an expression
  --> docs/guides/python-module-organization.md#block2.py:12:54
   |
10 | │   ├── entities.py         # Domain entities (streams, records)
11 | │   └── value_objects.py    # Domain value objects (table names, schemas)
12 | ├── application/             # 📤 Application services
   |                                                       ^
13 | │   ├── __init__.py
14 | │   ├── target.py           # Main Singer Target implementation
   |

invalid-syntax: Got unexpected token │
  --> docs/guides/python-module-organization.md#block2.py:13:1
   |
11 | │   └── value_objects.py    # Domain value objects (table names, schemas)
12 | ├── application/             # 📤 Application services
13 | │   ├── __init__.py
   | ^
14 | │   ├── target.py           # Main Singer Target implementation
15 | │   ├── handlers.py         # Message handlers (SCHEMA, RECORD, STATE)
   |

invalid-syntax: Got unexpected token ├
  --> docs/guides/python-module-organization.md#block2.py:13:5
   |
11 | │   └── value_objects.py    # Domain value objects (table names, schemas)
12 | ├── application/             # 📤 Application services
13 | │   ├── __init__.py
   |     ^
14 | │   ├── target.py           # Main Singer Target implementation
15 | │   ├── handlers.py         # Message handlers (SCHEMA, RECORD, STATE)
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block2.py:13:6
   |
11 | │   └── value_objects.py    # Domain value objects (table names, schemas)
12 | ├── application/             # 📤 Application services
13 | │   ├── __init__.py
   |      ^
14 | │   ├── target.py           # Main Singer Target implementation
15 | │   ├── handlers.py         # Message handlers (SCHEMA, RECORD, STATE)
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block2.py:13:7
   |
11 | │   └── value_objects.py    # Domain value objects (table names, schemas)
12 | ├── application/             # 📤 Application services
13 | │   ├── __init__.py
   |       ^
14 | │   ├── target.py           # Main Singer Target implementation
15 | │   ├── handlers.py         # Message handlers (SCHEMA, RECORD, STATE)
   |

invalid-syntax: Got unexpected token │
  --> docs/guides/python-module-organization.md#block2.py:14:1
   |
12 | ├── application/             # 📤 Application services
13 | │   ├── __init__.py
14 | │   ├── target.py           # Main Singer Target implementation
   | ^
15 | │   ├── handlers.py         # Message handlers (SCHEMA, RECORD, STATE)
16 | │   └── services.py         # Application services
   |

invalid-syntax: Got unexpected token ├
  --> docs/guides/python-module-organization.md#block2.py:14:5
   |
12 | ├── application/             # 📤 Application services
13 | │   ├── __init__.py
14 | │   ├── target.py           # Main Singer Target implementation
   |     ^
15 | │   ├── handlers.py         # Message handlers (SCHEMA, RECORD, STATE)
16 | │   └── services.py         # Application services
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block2.py:14:6
   |
12 | ├── application/             # 📤 Application services
13 | │   ├── __init__.py
14 | │   ├── target.py           # Main Singer Target implementation
   |      ^
15 | │   ├── handlers.py         # Message handlers (SCHEMA, RECORD, STATE)
16 | │   └── services.py         # Application services
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block2.py:14:7
   |
12 | ├── application/             # 📤 Application services
13 | │   ├── __init__.py
14 | │   ├── target.py           # Main Singer Target implementation
   |       ^
15 | │   ├── handlers.py         # Message handlers (SCHEMA, RECORD, STATE)
16 | │   └── services.py         # Application services
   |

invalid-syntax: Got unexpected token │
  --> docs/guides/python-module-organization.md#block2.py:15:1
   |
13 | │   ├── __init__.py
14 | │   ├── target.py           # Main Singer Target implementation
15 | │   ├── handlers.py         # Message handlers (SCHEMA, RECORD, STATE)
   | ^
16 | │   └── services.py         # Application services
17 | ├── infrastructure/         # 🔧 Infrastructure layer
   |

invalid-syntax: Got unexpected token ├
  --> docs/guides/python-module-organization.md#block2.py:15:5
   |
13 | │   ├── __init__.py
14 | │   ├── target.py           # Main Singer Target implementation
15 | │   ├── handlers.py         # Message handlers (SCHEMA, RECORD, STATE)
   |     ^
16 | │   └── services.py         # Application services
17 | ├── infrastructure/         # 🔧 Infrastructure layer
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block2.py:15:6
   |
13 | │   ├── __init__.py
14 | │   ├── target.py           # Main Singer Target implementation
15 | │   ├── handlers.py         # Message handlers (SCHEMA, RECORD, STATE)
   |      ^
16 | │   └── services.py         # Application services
17 | ├── infrastructure/         # 🔧 Infrastructure layer
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block2.py:15:7
   |
13 | │   ├── __init__.py
14 | │   ├── target.py           # Main Singer Target implementation
15 | │   ├── handlers.py         # Message handlers (SCHEMA, RECORD, STATE)
   |       ^
16 | │   └── services.py         # Application services
17 | ├── infrastructure/         # 🔧 Infrastructure layer
   |

invalid-syntax: Got unexpected token │
  --> docs/guides/python-module-organization.md#block2.py:16:1
   |
14 | │   ├── target.py           # Main Singer Target implementation
15 | │   ├── handlers.py         # Message handlers (SCHEMA, RECORD, STATE)
16 | │   └── services.py         # Application services
   | ^
17 | ├── infrastructure/         # 🔧 Infrastructure layer
18 | │   ├── __init__.py
   |

invalid-syntax: Got unexpected token └
  --> docs/guides/python-module-organization.md#block2.py:16:5
   |
14 | │   ├── target.py           # Main Singer Target implementation
15 | │   ├── handlers.py         # Message handlers (SCHEMA, RECORD, STATE)
16 | │   └── services.py         # Application services
   |     ^
17 | ├── infrastructure/         # 🔧 Infrastructure layer
18 | │   ├── __init__.py
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block2.py:16:6
   |
14 | │   ├── target.py           # Main Singer Target implementation
15 | │   ├── handlers.py         # Message handlers (SCHEMA, RECORD, STATE)
16 | │   └── services.py         # Application services
   |      ^
17 | ├── infrastructure/         # 🔧 Infrastructure layer
18 | │   ├── __init__.py
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block2.py:16:7
   |
14 | │   ├── target.py           # Main Singer Target implementation
15 | │   ├── handlers.py         # Message handlers (SCHEMA, RECORD, STATE)
16 | │   └── services.py         # Application services
   |       ^
17 | ├── infrastructure/         # 🔧 Infrastructure layer
18 | │   ├── __init__.py
   |

invalid-syntax: Got unexpected token ├
  --> docs/guides/python-module-organization.md#block2.py:17:1
   |
15 | │   ├── handlers.py         # Message handlers (SCHEMA, RECORD, STATE)
16 | │   └── services.py         # Application services
17 | ├── infrastructure/         # 🔧 Infrastructure layer
   | ^
18 | │   ├── __init__.py
19 | │   ├── loader.py           # Oracle data loading operations
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block2.py:17:2
   |
15 | │   ├── handlers.py         # Message handlers (SCHEMA, RECORD, STATE)
16 | │   └── services.py         # Application services
17 | ├── infrastructure/         # 🔧 Infrastructure layer
   |  ^
18 | │   ├── __init__.py
19 | │   ├── loader.py           # Oracle data loading operations
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block2.py:17:3
   |
15 | │   ├── handlers.py         # Message handlers (SCHEMA, RECORD, STATE)
16 | │   └── services.py         # Application services
17 | ├── infrastructure/         # 🔧 Infrastructure layer
   |   ^
18 | │   ├── __init__.py
19 | │   ├── loader.py           # Oracle data loading operations
   |

missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
  --> docs/guides/python-module-organization.md#block2.py:17:19
   |
15 | │   ├── handlers.py         # Message handlers (SCHEMA, RECORD, STATE)
16 | │   └── services.py         # Application services
17 | ├── infrastructure/         # 🔧 Infrastructure layer
   |                   ^
18 | │   ├── __init__.py
19 | │   ├── loader.py           # Oracle data loading operations
   |
help: Add missing whitespace

invalid-syntax: Expected an expression
  --> docs/guides/python-module-organization.md#block2.py:17:53
   |
15 | │   ├── handlers.py         # Message handlers (SCHEMA, RECORD, STATE)
16 | │   └── services.py         # Application services
17 | ├── infrastructure/         # 🔧 Infrastructure layer
   |                                                      ^
18 | │   ├── __init__.py
19 | │   ├── loader.py           # Oracle data loading operations
   |

invalid-syntax: Got unexpected token │
  --> docs/guides/python-module-organization.md#block2.py:18:1
   |
16 | │   └── services.py         # Application services
17 | ├── infrastructure/         # 🔧 Infrastructure layer
18 | │   ├── __init__.py
   | ^
19 | │   ├── loader.py           # Oracle data loading operations
20 | │   ├── repository.py       # Data persistence (if needed)
   |

invalid-syntax: Got unexpected token ├
  --> docs/guides/python-module-organization.md#block2.py:18:5
   |
16 | │   └── services.py         # Application services
17 | ├── infrastructure/         # 🔧 Infrastructure layer
18 | │   ├── __init__.py
   |     ^
19 | │   ├── loader.py           # Oracle data loading operations
20 | │   ├── repository.py       # Data persistence (if needed)
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block2.py:18:6
   |
16 | │   └── services.py         # Application services
17 | ├── infrastructure/         # 🔧 Infrastructure layer
18 | │   ├── __init__.py
   |      ^
19 | │   ├── loader.py           # Oracle data loading operations
20 | │   ├── repository.py       # Data persistence (if needed)
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block2.py:18:7
   |
16 | │   └── services.py         # Application services
17 | ├── infrastructure/         # 🔧 Infrastructure layer
18 | │   ├── __init__.py
   |       ^
19 | │   ├── loader.py           # Oracle data loading operations
20 | │   ├── repository.py       # Data persistence (if needed)
   |

invalid-syntax: Got unexpected token │
  --> docs/guides/python-module-organization.md#block2.py:19:1
   |
17 | ├── infrastructure/         # 🔧 Infrastructure layer
18 | │   ├── __init__.py
19 | │   ├── loader.py           # Oracle data loading operations
   | ^
20 | │   ├── repository.py       # Data persistence (if needed)
21 | │   └── adapters.py         # External service adapters
   |

invalid-syntax: Got unexpected token ├
  --> docs/guides/python-module-organization.md#block2.py:19:5
   |
17 | ├── infrastructure/         # 🔧 Infrastructure layer
18 | │   ├── __init__.py
19 | │   ├── loader.py           # Oracle data loading operations
   |     ^
20 | │   ├── repository.py       # Data persistence (if needed)
21 | │   └── adapters.py         # External service adapters
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block2.py:19:6
   |
17 | ├── infrastructure/         # 🔧 Infrastructure layer
18 | │   ├── __init__.py
19 | │   ├── loader.py           # Oracle data loading operations
   |      ^
20 | │   ├── repository.py       # Data persistence (if needed)
21 | │   └── adapters.py         # External service adapters
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block2.py:19:7
   |
17 | ├── infrastructure/         # 🔧 Infrastructure layer
18 | │   ├── __init__.py
19 | │   ├── loader.py           # Oracle data loading operations
   |       ^
20 | │   ├── repository.py       # Data persistence (if needed)
21 | │   └── adapters.py         # External service adapters
   |

invalid-syntax: Got unexpected token │
  --> docs/guides/python-module-organization.md#block2.py:20:1
   |
18 | │   ├── __init__.py
19 | │   ├── loader.py           # Oracle data loading operations
20 | │   ├── repository.py       # Data persistence (if needed)
   | ^
21 | │   └── adapters.py         # External service adapters
22 | └── exceptions.py           # 🚨 Complete error hierarchy
   |

invalid-syntax: Got unexpected token ├
  --> docs/guides/python-module-organization.md#block2.py:20:5
   |
18 | │   ├── __init__.py
19 | │   ├── loader.py           # Oracle data loading operations
20 | │   ├── repository.py       # Data persistence (if needed)
   |     ^
21 | │   └── adapters.py         # External service adapters
22 | └── exceptions.py           # 🚨 Complete error hierarchy
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block2.py:20:6
   |
18 | │   ├── __init__.py
19 | │   ├── loader.py           # Oracle data loading operations
20 | │   ├── repository.py       # Data persistence (if needed)
   |      ^
21 | │   └── adapters.py         # External service adapters
22 | └── exceptions.py           # 🚨 Complete error hierarchy
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block2.py:20:7
   |
18 | │   ├── __init__.py
19 | │   ├── loader.py           # Oracle data loading operations
20 | │   ├── repository.py       # Data persistence (if needed)
   |       ^
21 | │   └── adapters.py         # External service adapters
22 | └── exceptions.py           # 🚨 Complete error hierarchy
   |

invalid-syntax: Got unexpected token │
  --> docs/guides/python-module-organization.md#block2.py:21:1
   |
19 | │   ├── loader.py           # Oracle data loading operations
20 | │   ├── repository.py       # Data persistence (if needed)
21 | │   └── adapters.py         # External service adapters
   | ^
22 | └── exceptions.py           # 🚨 Complete error hierarchy
   |

invalid-syntax: Got unexpected token └
  --> docs/guides/python-module-organization.md#block2.py:21:5
   |
19 | │   ├── loader.py           # Oracle data loading operations
20 | │   ├── repository.py       # Data persistence (if needed)
21 | │   └── adapters.py         # External service adapters
   |     ^
22 | └── exceptions.py           # 🚨 Complete error hierarchy
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block2.py:21:6
   |
19 | │   ├── loader.py           # Oracle data loading operations
20 | │   ├── repository.py       # Data persistence (if needed)
21 | │   └── adapters.py         # External service adapters
   |      ^
22 | └── exceptions.py           # 🚨 Complete error hierarchy
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block2.py:21:7
   |
19 | │   ├── loader.py           # Oracle data loading operations
20 | │   ├── repository.py       # Data persistence (if needed)
21 | │   └── adapters.py         # External service adapters
   |       ^
22 | └── exceptions.py           # 🚨 Complete error hierarchy
   |

invalid-syntax: Got unexpected token └
  --> docs/guides/python-module-organization.md#block2.py:22:1
   |
20 | │   ├── repository.py       # Data persistence (if needed)
21 | │   └── adapters.py         # External service adapters
22 | └── exceptions.py           # 🚨 Complete error hierarchy
   | ^

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block2.py:22:2
   |
20 | │   ├── repository.py       # Data persistence (if needed)
21 | │   └── adapters.py         # External service adapters
22 | └── exceptions.py           # 🚨 Complete error hierarchy
   |  ^

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block2.py:22:3
   |
20 | │   ├── repository.py       # Data persistence (if needed)
21 | │   └── adapters.py         # External service adapters
22 | └── exceptions.py           # 🚨 Complete error hierarchy
   |   ^

Found 89 errors. |
| docs/guides/python-module-organization.md | python_codeblock | medium | block #3: missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
 --> docs/guides/python-module-organization.md#block3.py:1:4
  |
1 | src/flext_target_oracle/
  |    ^
2 | ├── __init__.py              # 🎯 Clean exports (fixed)
3 | ├── settings.py                # ⚙️ Enhanced configuration
  |
help: Add missing whitespace

missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
 --> docs/guides/python-module-organization.md#block3.py:1:24
  |
1 | src/flext_target_oracle/
  |                        ^
2 | ├── __init__.py              # 🎯 Clean exports (fixed)
3 | ├── settings.py                # ⚙️ Enhanced configuration
  |
help: Add missing whitespace

invalid-syntax: Expected an expression
 --> docs/guides/python-module-organization.md#block3.py:1:25
  |
1 | src/flext_target_oracle/
  |                         ^
2 | ├── __init__.py              # 🎯 Clean exports (fixed)
3 | ├── settings.py                # ⚙️ Enhanced configuration
  |

invalid-syntax: Got unexpected token ├
 --> docs/guides/python-module-organization.md#block3.py:2:1
  |
1 | src/flext_target_oracle/
2 | ├── __init__.py              # 🎯 Clean exports (fixed)
  | ^
3 | ├── settings.py                # ⚙️ Enhanced configuration
4 | ├── target.py                # 🎯 Singer-compliant implementation (fixed)
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block3.py:2:2
  |
1 | src/flext_target_oracle/
2 | ├── __init__.py              # 🎯 Clean exports (fixed)
  |  ^
3 | ├── settings.py                # ⚙️ Enhanced configuration
4 | ├── target.py                # 🎯 Singer-compliant implementation (fixed)
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block3.py:2:3
  |
1 | src/flext_target_oracle/
2 | ├── __init__.py              # 🎯 Clean exports (fixed)
  |   ^
3 | ├── settings.py                # ⚙️ Enhanced configuration
4 | ├── target.py                # 🎯 Singer-compliant implementation (fixed)
  |

invalid-syntax: Got unexpected token ├
 --> docs/guides/python-module-organization.md#block3.py:3:1
  |
1 | src/flext_target_oracle/
2 | ├── __init__.py              # 🎯 Clean exports (fixed)
3 | ├── settings.py                # ⚙️ Enhanced configuration
  | ^
4 | ├── target.py                # 🎯 Singer-compliant implementation (fixed)
5 | ├── loader.py                # 🔧 Secure data loading (fixed)
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block3.py:3:2
  |
1 | src/flext_target_oracle/
2 | ├── __init__.py              # 🎯 Clean exports (fixed)
3 | ├── settings.py                # ⚙️ Enhanced configuration
  |  ^
4 | ├── target.py                # 🎯 Singer-compliant implementation (fixed)
5 | ├── loader.py                # 🔧 Secure data loading (fixed)
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block3.py:3:3
  |
1 | src/flext_target_oracle/
2 | ├── __init__.py              # 🎯 Clean exports (fixed)
3 | ├── settings.py                # ⚙️ Enhanced configuration
  |   ^
4 | ├── target.py                # 🎯 Singer-compliant implementation (fixed)
5 | ├── loader.py                # 🔧 Secure data loading (fixed)
  |

invalid-syntax: Got unexpected token ├
 --> docs/guides/python-module-organization.md#block3.py:4:1
  |
2 | ├── __init__.py              # 🎯 Clean exports (fixed)
3 | ├── settings.py                # ⚙️ Enhanced configuration
4 | ├── target.py                # 🎯 Singer-compliant implementation (fixed)
  | ^
5 | ├── loader.py                # 🔧 Secure data loading (fixed)
6 | └── exceptions.py            # 🚨 Single source of exceptions (fixed)
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block3.py:4:2
  |
2 | ├── __init__.py              # 🎯 Clean exports (fixed)
3 | ├── settings.py                # ⚙️ Enhanced configuration
4 | ├── target.py                # 🎯 Singer-compliant implementation (fixed)
  |  ^
5 | ├── loader.py                # 🔧 Secure data loading (fixed)
6 | └── exceptions.py            # 🚨 Single source of exceptions (fixed)
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block3.py:4:3
  |
2 | ├── __init__.py              # 🎯 Clean exports (fixed)
3 | ├── settings.py                # ⚙️ Enhanced configuration
4 | ├── target.py                # 🎯 Singer-compliant implementation (fixed)
  |   ^
5 | ├── loader.py                # 🔧 Secure data loading (fixed)
6 | └── exceptions.py            # 🚨 Single source of exceptions (fixed)
  |

invalid-syntax: Got unexpected token ├
 --> docs/guides/python-module-organization.md#block3.py:5:1
  |
3 | ├── settings.py                # ⚙️ Enhanced configuration
4 | ├── target.py                # 🎯 Singer-compliant implementation (fixed)
5 | ├── loader.py                # 🔧 Secure data loading (fixed)
  | ^
6 | └── exceptions.py            # 🚨 Single source of exceptions (fixed)
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block3.py:5:2
  |
3 | ├── settings.py                # ⚙️ Enhanced configuration
4 | ├── target.py                # 🎯 Singer-compliant implementation (fixed)
5 | ├── loader.py                # 🔧 Secure data loading (fixed)
  |  ^
6 | └── exceptions.py            # 🚨 Single source of exceptions (fixed)
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block3.py:5:3
  |
3 | ├── settings.py                # ⚙️ Enhanced configuration
4 | ├── target.py                # 🎯 Singer-compliant implementation (fixed)
5 | ├── loader.py                # 🔧 Secure data loading (fixed)
  |   ^
6 | └── exceptions.py            # 🚨 Single source of exceptions (fixed)
  |

invalid-syntax: Got unexpected token └
 --> docs/guides/python-module-organization.md#block3.py:6:1
  |
4 | ├── target.py                # 🎯 Singer-compliant implementation (fixed)
5 | ├── loader.py                # 🔧 Secure data loading (fixed)
6 | └── exceptions.py            # 🚨 Single source of exceptions (fixed)
  | ^

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block3.py:6:2
  |
4 | ├── target.py                # 🎯 Singer-compliant implementation (fixed)
5 | ├── loader.py                # 🔧 Secure data loading (fixed)
6 | └── exceptions.py            # 🚨 Single source of exceptions (fixed)
  |  ^

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block3.py:6:3
  |
4 | ├── target.py                # 🎯 Singer-compliant implementation (fixed)
5 | ├── loader.py                # 🔧 Secure data loading (fixed)
6 | └── exceptions.py            # 🚨 Single source of exceptions (fixed)
  |   ^

Found 18 errors. |
| docs/guides/python-module-organization.md | python_codeblock | medium | block #4: blank-lines-top-level: Expected 2 blank lines, found 0
  --> docs/guides/python-module-organization.md#block4.py:12:1
   |
10 | )
11 | # ✅ CORRECT - Comprehensive validation with domain rules
12 | class FlextOracleTargetSettings(m.Value):
   | ^^^^^
13 |     """Type-safe configuration with business validation."""
   |
help: Add missing blank line(s)

invalid-syntax: Expected an identifier
  --> docs/guides/python-module-organization.md#block4.py:38:24
   |
36 |                 return result
37 |
38 |         return r[bool].| ok(value=True)
   |                        ^
39 |
40 | # ❌ INCORRECT - Plain dataclass without validation
   |

missing-whitespace-around-bitwise-or-shift-operator: Missing whitespace around bitwise or shift operator
  --> docs/guides/python-module-organization.md#block4.py:38:24
   |
36 |                 return result
37 |
38 |         return r[bool].| ok(value=True)
   |                        ^
39 |
40 | # ❌ INCORRECT - Plain dataclass without validation
   |
help: Add missing whitespace

blank-lines-top-level: Expected 2 blank lines, found 1
  --> docs/guides/python-module-organization.md#block4.py:41:1
   |
40 | # ❌ INCORRECT - Plain dataclass without validation
41 | @dataclass
   | ^
42 | class BadConfig:
43 |     oracle_host: str
   |
help: Add missing blank line(s)

Found 4 errors. |
| docs/guides/python-module-organization.md | python_codeblock | medium | block #5: invalid-syntax: Got unexpected token ┌
 --> docs/guides/python-module-organization.md#block5.py:2:1
  |
1 | # ✅ CORRECT - Dependencies flow inward
2 | ┌─────────────────────────────┐
  | ^
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:2:2
  |
1 | # ✅ CORRECT - Dependencies flow inward
2 | ┌─────────────────────────────┐
  |  ^
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:2:3
  |
1 | # ✅ CORRECT - Dependencies flow inward
2 | ┌─────────────────────────────┐
  |   ^
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:2:4
  |
1 | # ✅ CORRECT - Dependencies flow inward
2 | ┌─────────────────────────────┐
  |    ^
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:2:5
  |
1 | # ✅ CORRECT - Dependencies flow inward
2 | ┌─────────────────────────────┐
  |     ^
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:2:6
  |
1 | # ✅ CORRECT - Dependencies flow inward
2 | ┌─────────────────────────────┐
  |      ^
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:2:7
  |
1 | # ✅ CORRECT - Dependencies flow inward
2 | ┌─────────────────────────────┐
  |       ^
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:2:8
  |
1 | # ✅ CORRECT - Dependencies flow inward
2 | ┌─────────────────────────────┐
  |        ^
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:2:9
  |
1 | # ✅ CORRECT - Dependencies flow inward
2 | ┌─────────────────────────────┐
  |         ^
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:2:10
  |
1 | # ✅ CORRECT - Dependencies flow inward
2 | ┌─────────────────────────────┐
  |          ^
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:2:11
  |
1 | # ✅ CORRECT - Dependencies flow inward
2 | ┌─────────────────────────────┐
  |           ^
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:2:12
  |
1 | # ✅ CORRECT - Dependencies flow inward
2 | ┌─────────────────────────────┐
  |            ^
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:2:13
  |
1 | # ✅ CORRECT - Dependencies flow inward
2 | ┌─────────────────────────────┐
  |             ^
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:2:14
  |
1 | # ✅ CORRECT - Dependencies flow inward
2 | ┌─────────────────────────────┐
  |              ^
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:2:15
  |
1 | # ✅ CORRECT - Dependencies flow inward
2 | ┌─────────────────────────────┐
  |               ^
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:2:16
  |
1 | # ✅ CORRECT - Dependencies flow inward
2 | ┌─────────────────────────────┐
  |                ^
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:2:17
  |
1 | # ✅ CORRECT - Dependencies flow inward
2 | ┌─────────────────────────────┐
  |                 ^
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:2:18
  |
1 | # ✅ CORRECT - Dependencies flow inward
2 | ┌─────────────────────────────┐
  |                  ^
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:2:19
  |
1 | # ✅ CORRECT - Dependencies flow inward
2 | ┌─────────────────────────────┐
  |                   ^
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:2:20
  |
1 | # ✅ CORRECT - Dependencies flow inward
2 | ┌─────────────────────────────┐
  |                    ^
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:2:21
  |
1 | # ✅ CORRECT - Dependencies flow inward
2 | ┌─────────────────────────────┐
  |                     ^
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:2:22
  |
1 | # ✅ CORRECT - Dependencies flow inward
2 | ┌─────────────────────────────┐
  |                      ^
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:2:23
  |
1 | # ✅ CORRECT - Dependencies flow inward
2 | ┌─────────────────────────────┐
  |                       ^
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:2:24
  |
1 | # ✅ CORRECT - Dependencies flow inward
2 | ┌─────────────────────────────┐
  |                        ^
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:2:25
  |
1 | # ✅ CORRECT - Dependencies flow inward
2 | ┌─────────────────────────────┐
  |                         ^
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:2:26
  |
1 | # ✅ CORRECT - Dependencies flow inward
2 | ┌─────────────────────────────┐
  |                          ^
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:2:27
  |
1 | # ✅ CORRECT - Dependencies flow inward
2 | ┌─────────────────────────────┐
  |                           ^
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:2:28
  |
1 | # ✅ CORRECT - Dependencies flow inward
2 | ┌─────────────────────────────┐
  |                            ^
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:2:29
  |
1 | # ✅ CORRECT - Dependencies flow inward
2 | ┌─────────────────────────────┐
  |                             ^
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:2:30
  |
1 | # ✅ CORRECT - Dependencies flow inward
2 | ┌─────────────────────────────┐
  |                              ^
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
  |

invalid-syntax: Got unexpected token ┐
 --> docs/guides/python-module-organization.md#block5.py:2:31
  |
1 | # ✅ CORRECT - Dependencies flow inward
2 | ┌─────────────────────────────┐
  |                               ^
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
  |

invalid-syntax: Got unexpected token │
 --> docs/guides/python-module-organization.md#block5.py:3:1
  |
1 | # ✅ CORRECT - Dependencies flow inward
2 | ┌─────────────────────────────┐
3 | │     target.py               │  # Application Layer
  | ^
4 | │  (Singer Implementation)    │
5 | ├─────────────────────────────┤  ↓ depends on
  |

invalid-syntax: Got unexpected token │
 --> docs/guides/python-module-organization.md#block5.py:3:31
  |
1 | # ✅ CORRECT - Dependencies flow inward
2 | ┌─────────────────────────────┐
3 | │     target.py               │  # Application Layer
  |                               ^
4 | │  (Singer Implementation)    │
5 | ├─────────────────────────────┤  ↓ depends on
  |

invalid-syntax: Expected a statement
 --> docs/guides/python-module-organization.md#block5.py:3:53
  |
1 | # ✅ CORRECT - Dependencies flow inward
2 | ┌─────────────────────────────┐
3 | │     target.py               │  # Application Layer
  |                                                     ^
4 | │  (Singer Implementation)    │
5 | ├─────────────────────────────┤  ↓ depends on
  |

invalid-syntax: Got unexpected token │
 --> docs/guides/python-module-organization.md#block5.py:4:1
  |
2 | ┌─────────────────────────────┐
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
  | ^
5 | ├─────────────────────────────┤  ↓ depends on
6 | │     settings.py               │  # Domain Layer
  |

invalid-syntax: Expected `)`, found identifier
 --> docs/guides/python-module-organization.md#block5.py:4:12
  |
2 | ┌─────────────────────────────┐
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
  |            ^^^^^^^^^^^^^^
5 | ├─────────────────────────────┤  ↓ depends on
6 | │     settings.py               │  # Domain Layer
  |

invalid-syntax: Expected a statement
 --> docs/guides/python-module-organization.md#block5.py:4:26
  |
2 | ┌─────────────────────────────┐
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
  |                          ^
5 | ├─────────────────────────────┤  ↓ depends on
6 | │     settings.py               │  # Domain Layer
  |

invalid-syntax: Got unexpected token │
 --> docs/guides/python-module-organization.md#block5.py:4:31
  |
2 | ┌─────────────────────────────┐
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
  |                               ^
5 | ├─────────────────────────────┤  ↓ depends on
6 | │     settings.py               │  # Domain Layer
  |

invalid-syntax: Expected a statement
 --> docs/guides/python-module-organization.md#block5.py:4:32
  |
2 | ┌─────────────────────────────┐
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
  |                                ^
5 | ├─────────────────────────────┤  ↓ depends on
6 | │     settings.py               │  # Domain Layer
  |

invalid-syntax: Got unexpected token ├
 --> docs/guides/python-module-organization.md#block5.py:5:1
  |
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
5 | ├─────────────────────────────┤  ↓ depends on
  | ^
6 | │     settings.py               │  # Domain Layer
7 | │  (Business Configuration)   │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:5:2
  |
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
5 | ├─────────────────────────────┤  ↓ depends on
  |  ^
6 | │     settings.py               │  # Domain Layer
7 | │  (Business Configuration)   │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:5:3
  |
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
5 | ├─────────────────────────────┤  ↓ depends on
  |   ^
6 | │     settings.py               │  # Domain Layer
7 | │  (Business Configuration)   │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:5:4
  |
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
5 | ├─────────────────────────────┤  ↓ depends on
  |    ^
6 | │     settings.py               │  # Domain Layer
7 | │  (Business Configuration)   │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:5:5
  |
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
5 | ├─────────────────────────────┤  ↓ depends on
  |     ^
6 | │     settings.py               │  # Domain Layer
7 | │  (Business Configuration)   │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:5:6
  |
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
5 | ├─────────────────────────────┤  ↓ depends on
  |      ^
6 | │     settings.py               │  # Domain Layer
7 | │  (Business Configuration)   │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:5:7
  |
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
5 | ├─────────────────────────────┤  ↓ depends on
  |       ^
6 | │     settings.py               │  # Domain Layer
7 | │  (Business Configuration)   │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:5:8
  |
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
5 | ├─────────────────────────────┤  ↓ depends on
  |        ^
6 | │     settings.py               │  # Domain Layer
7 | │  (Business Configuration)   │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:5:9
  |
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
5 | ├─────────────────────────────┤  ↓ depends on
  |         ^
6 | │     settings.py               │  # Domain Layer
7 | │  (Business Configuration)   │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:5:10
  |
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
5 | ├─────────────────────────────┤  ↓ depends on
  |          ^
6 | │     settings.py               │  # Domain Layer
7 | │  (Business Configuration)   │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:5:11
  |
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
5 | ├─────────────────────────────┤  ↓ depends on
  |           ^
6 | │     settings.py               │  # Domain Layer
7 | │  (Business Configuration)   │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:5:12
  |
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
5 | ├─────────────────────────────┤  ↓ depends on
  |            ^
6 | │     settings.py               │  # Domain Layer
7 | │  (Business Configuration)   │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:5:13
  |
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
5 | ├─────────────────────────────┤  ↓ depends on
  |             ^
6 | │     settings.py               │  # Domain Layer
7 | │  (Business Configuration)   │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:5:14
  |
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
5 | ├─────────────────────────────┤  ↓ depends on
  |              ^
6 | │     settings.py               │  # Domain Layer
7 | │  (Business Configuration)   │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:5:15
  |
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
5 | ├─────────────────────────────┤  ↓ depends on
  |               ^
6 | │     settings.py               │  # Domain Layer
7 | │  (Business Configuration)   │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:5:16
  |
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
5 | ├─────────────────────────────┤  ↓ depends on
  |                ^
6 | │     settings.py               │  # Domain Layer
7 | │  (Business Configuration)   │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:5:17
  |
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
5 | ├─────────────────────────────┤  ↓ depends on
  |                 ^
6 | │     settings.py               │  # Domain Layer
7 | │  (Business Configuration)   │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:5:18
  |
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
5 | ├─────────────────────────────┤  ↓ depends on
  |                  ^
6 | │     settings.py               │  # Domain Layer
7 | │  (Business Configuration)   │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:5:19
  |
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
5 | ├─────────────────────────────┤  ↓ depends on
  |                   ^
6 | │     settings.py               │  # Domain Layer
7 | │  (Business Configuration)   │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:5:20
  |
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
5 | ├─────────────────────────────┤  ↓ depends on
  |                    ^
6 | │     settings.py               │  # Domain Layer
7 | │  (Business Configuration)   │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:5:21
  |
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
5 | ├─────────────────────────────┤  ↓ depends on
  |                     ^
6 | │     settings.py               │  # Domain Layer
7 | │  (Business Configuration)   │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:5:22
  |
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
5 | ├─────────────────────────────┤  ↓ depends on
  |                      ^
6 | │     settings.py               │  # Domain Layer
7 | │  (Business Configuration)   │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:5:23
  |
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
5 | ├─────────────────────────────┤  ↓ depends on
  |                       ^
6 | │     settings.py               │  # Domain Layer
7 | │  (Business Configuration)   │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:5:24
  |
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
5 | ├─────────────────────────────┤  ↓ depends on
  |                        ^
6 | │     settings.py               │  # Domain Layer
7 | │  (Business Configuration)   │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:5:25
  |
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
5 | ├─────────────────────────────┤  ↓ depends on
  |                         ^
6 | │     settings.py               │  # Domain Layer
7 | │  (Business Configuration)   │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:5:26
  |
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
5 | ├─────────────────────────────┤  ↓ depends on
  |                          ^
6 | │     settings.py               │  # Domain Layer
7 | │  (Business Configuration)   │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:5:27
  |
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
5 | ├─────────────────────────────┤  ↓ depends on
  |                           ^
6 | │     settings.py               │  # Domain Layer
7 | │  (Business Configuration)   │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:5:28
  |
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
5 | ├─────────────────────────────┤  ↓ depends on
  |                            ^
6 | │     settings.py               │  # Domain Layer
7 | │  (Business Configuration)   │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:5:29
  |
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
5 | ├─────────────────────────────┤  ↓ depends on
  |                             ^
6 | │     settings.py               │  # Domain Layer
7 | │  (Business Configuration)   │
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block5.py:5:30
  |
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
5 | ├─────────────────────────────┤  ↓ depends on
  |                              ^
6 | │     settings.py               │  # Domain Layer
7 | │  (Business Configuration)   │
  |

invalid-syntax: Got unexpected token ┤
 --> docs/guides/python-module-organization.md#block5.py:5:31
  |
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
5 | ├─────────────────────────────┤  ↓ depends on
  |                               ^
6 | │     settings.py               │  # Domain Layer
7 | │  (Business Configuration)   │
  |

invalid-syntax: Got unexpected token ↓
 --> docs/guides/python-module-organization.md#block5.py:5:34
  |
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
5 | ├─────────────────────────────┤  ↓ depends on
  |                                  ^
6 | │     settings.py               │  # Domain Layer
7 | │  (Business Configuration)   │
  |

invalid-syntax: Simple statements must be separated by newlines or semicolons
 --> docs/guides/python-module-organization.md#block5.py:5:44
  |
3 | │     target.py               │  # Application Layer
4 | │  (Singer Implementation)    │
5 | ├─────────────────────────────┤  ↓ depends on
  |                                            ^^
6 | │     settings.py               │  # Domain Layer
7 | │  (Business Configuration)   │
  |

invalid-syntax: Got unexpected token │
 --> docs/guides/python-module-organization.md#block5.py:6:1
  |
4 | │  (Singer Implementation)    │
5 | ├─────────────────────────────┤  ↓ depends on
6 | │     settings.py               │  # Domain Layer
  | ^
7 | │  (Business Configuration)   │
8 | ├─────────────────────────────┤  ↓ depends on
  |

invalid-syntax: Got unexpected token │
 --> docs/guides/python-module-organization.md#block5.py:6:33
  |
4 | │  (Singer Implementation)    │
5 | ├─────────────────────────────┤  ↓ depends on
6 | │     settings.py               │  # Domain Layer
  |                                 ^
7 | │  (Business Configuration)   │
8 | ├─────────────────────────────┤  ↓ depends on
  |

invalid-syntax: Expected a statement
 --> docs/guides/python-module-organization.md#block5.py:6:50
  |
4 | │  (Singer Implementation)    │
5 | ├─────────────────────────────┤  ↓ depends on
6 | │     settings.py               │  # Domain Layer
  |                                                  ^
7 | │  (Business Configuration)   │
8 | ├─────────────────────────────┤  ↓ depends on
  |

invalid-syntax: Got unexpected token │
 --> docs/guides/python-module-organization.md#block5.py:7:1
  |
5 | ├─────────────────────────────┤  ↓ depends on
6 | │     settings.py               │  # Domain Layer
7 | │  (Business Configuration)   │
  | ^
8 | ├─────────────────────────────┤  ↓ depends on
9 | │     loader.py               │  # Infrastructure Layer
  |

invalid-syntax: Expected `)`, found identifier
 --> docs/guides/python-module-organization.md#block5.py:7:14
  |
5 | ├─────────────────────────────┤  ↓ depends on
6 | │     settings.py               │  # Domain Layer
7 | │  (Business Configuration)   │
  |              ^^^^^^^^^^^^^
8 | ├─────────────────────────────┤  ↓ depends on
9 | │     loader.py               │  # Infrastructure Layer
  |

invalid-syntax: Expected a statement
 --> docs/guides/python-module-organization.md#block5.py:7:27
  |
5 | ├─────────────────────────────┤  ↓ depends on
6 | │     settings.py               │  # Domain Layer
7 | │  (Business Configuration)   │
  |                           ^
8 | ├─────────────────────────────┤  ↓ depends on
9 | │     loader.py               │  # Infrastructure Layer
  |

invalid-syntax: Got unexpected token │
 --> docs/guides/python-module-organization.md#block5.py:7:31
  |
5 | ├─────────────────────────────┤  ↓ depends on
6 | │     settings.py               │  # Domain Layer
7 | │  (Business Configuration)   │
  |                               ^
8 | ├─────────────────────────────┤  ↓ depends on
9 | │     loader.py               │  # Infrastructure Layer
  |

invalid-syntax: Expected a statement
 --> docs/guides/python-module-organization.md#block5.py:7:32
  |
5 | ├─────────────────────────────┤  ↓ depends on
6 | │     settings.py               │  # Domain Layer
7 | │  (Business Configuration)   │
  |                                ^
8 | ├─────────────────────────────┤  ↓ depends on
9 | │     loader.py               │  # Infrastructure Layer
  |

invalid-syntax: Got unexpected token ├
  --> docs/guides/python-module-organization.md#block5.py:8:1
   |
 6 | │     settings.py               │  # Domain Layer
 7 | │  (Business Configuration)   │
 8 | ├─────────────────────────────┤  ↓ depends on
   | ^
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:8:2
   |
 6 | │     settings.py               │  # Domain Layer
 7 | │  (Business Configuration)   │
 8 | ├─────────────────────────────┤  ↓ depends on
   |  ^
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:8:3
   |
 6 | │     settings.py               │  # Domain Layer
 7 | │  (Business Configuration)   │
 8 | ├─────────────────────────────┤  ↓ depends on
   |   ^
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:8:4
   |
 6 | │     settings.py               │  # Domain Layer
 7 | │  (Business Configuration)   │
 8 | ├─────────────────────────────┤  ↓ depends on
   |    ^
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:8:5
   |
 6 | │     settings.py               │  # Domain Layer
 7 | │  (Business Configuration)   │
 8 | ├─────────────────────────────┤  ↓ depends on
   |     ^
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:8:6
   |
 6 | │     settings.py               │  # Domain Layer
 7 | │  (Business Configuration)   │
 8 | ├─────────────────────────────┤  ↓ depends on
   |      ^
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:8:7
   |
 6 | │     settings.py               │  # Domain Layer
 7 | │  (Business Configuration)   │
 8 | ├─────────────────────────────┤  ↓ depends on
   |       ^
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:8:8
   |
 6 | │     settings.py               │  # Domain Layer
 7 | │  (Business Configuration)   │
 8 | ├─────────────────────────────┤  ↓ depends on
   |        ^
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:8:9
   |
 6 | │     settings.py               │  # Domain Layer
 7 | │  (Business Configuration)   │
 8 | ├─────────────────────────────┤  ↓ depends on
   |         ^
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:8:10
   |
 6 | │     settings.py               │  # Domain Layer
 7 | │  (Business Configuration)   │
 8 | ├─────────────────────────────┤  ↓ depends on
   |          ^
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:8:11
   |
 6 | │     settings.py               │  # Domain Layer
 7 | │  (Business Configuration)   │
 8 | ├─────────────────────────────┤  ↓ depends on
   |           ^
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:8:12
   |
 6 | │     settings.py               │  # Domain Layer
 7 | │  (Business Configuration)   │
 8 | ├─────────────────────────────┤  ↓ depends on
   |            ^
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:8:13
   |
 6 | │     settings.py               │  # Domain Layer
 7 | │  (Business Configuration)   │
 8 | ├─────────────────────────────┤  ↓ depends on
   |             ^
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:8:14
   |
 6 | │     settings.py               │  # Domain Layer
 7 | │  (Business Configuration)   │
 8 | ├─────────────────────────────┤  ↓ depends on
   |              ^
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:8:15
   |
 6 | │     settings.py               │  # Domain Layer
 7 | │  (Business Configuration)   │
 8 | ├─────────────────────────────┤  ↓ depends on
   |               ^
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:8:16
   |
 6 | │     settings.py               │  # Domain Layer
 7 | │  (Business Configuration)   │
 8 | ├─────────────────────────────┤  ↓ depends on
   |                ^
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:8:17
   |
 6 | │     settings.py               │  # Domain Layer
 7 | │  (Business Configuration)   │
 8 | ├─────────────────────────────┤  ↓ depends on
   |                 ^
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:8:18
   |
 6 | │     settings.py               │  # Domain Layer
 7 | │  (Business Configuration)   │
 8 | ├─────────────────────────────┤  ↓ depends on
   |                  ^
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:8:19
   |
 6 | │     settings.py               │  # Domain Layer
 7 | │  (Business Configuration)   │
 8 | ├─────────────────────────────┤  ↓ depends on
   |                   ^
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:8:20
   |
 6 | │     settings.py               │  # Domain Layer
 7 | │  (Business Configuration)   │
 8 | ├─────────────────────────────┤  ↓ depends on
   |                    ^
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:8:21
   |
 6 | │     settings.py               │  # Domain Layer
 7 | │  (Business Configuration)   │
 8 | ├─────────────────────────────┤  ↓ depends on
   |                     ^
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:8:22
   |
 6 | │     settings.py               │  # Domain Layer
 7 | │  (Business Configuration)   │
 8 | ├─────────────────────────────┤  ↓ depends on
   |                      ^
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:8:23
   |
 6 | │     settings.py               │  # Domain Layer
 7 | │  (Business Configuration)   │
 8 | ├─────────────────────────────┤  ↓ depends on
   |                       ^
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:8:24
   |
 6 | │     settings.py               │  # Domain Layer
 7 | │  (Business Configuration)   │
 8 | ├─────────────────────────────┤  ↓ depends on
   |                        ^
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:8:25
   |
 6 | │     settings.py               │  # Domain Layer
 7 | │  (Business Configuration)   │
 8 | ├─────────────────────────────┤  ↓ depends on
   |                         ^
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:8:26
   |
 6 | │     settings.py               │  # Domain Layer
 7 | │  (Business Configuration)   │
 8 | ├─────────────────────────────┤  ↓ depends on
   |                          ^
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:8:27
   |
 6 | │     settings.py               │  # Domain Layer
 7 | │  (Business Configuration)   │
 8 | ├─────────────────────────────┤  ↓ depends on
   |                           ^
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:8:28
   |
 6 | │     settings.py               │  # Domain Layer
 7 | │  (Business Configuration)   │
 8 | ├─────────────────────────────┤  ↓ depends on
   |                            ^
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:8:29
   |
 6 | │     settings.py               │  # Domain Layer
 7 | │  (Business Configuration)   │
 8 | ├─────────────────────────────┤  ↓ depends on
   |                             ^
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:8:30
   |
 6 | │     settings.py               │  # Domain Layer
 7 | │  (Business Configuration)   │
 8 | ├─────────────────────────────┤  ↓ depends on
   |                              ^
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
   |

invalid-syntax: Got unexpected token ┤
  --> docs/guides/python-module-organization.md#block5.py:8:31
   |
 6 | │     settings.py               │  # Domain Layer
 7 | │  (Business Configuration)   │
 8 | ├─────────────────────────────┤  ↓ depends on
   |                               ^
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
   |

invalid-syntax: Got unexpected token ↓
  --> docs/guides/python-module-organization.md#block5.py:8:34
   |
 6 | │     settings.py               │  # Domain Layer
 7 | │  (Business Configuration)   │
 8 | ├─────────────────────────────┤  ↓ depends on
   |                                  ^
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
   |

invalid-syntax: Simple statements must be separated by newlines or semicolons
  --> docs/guides/python-module-organization.md#block5.py:8:44
   |
 6 | │     settings.py               │  # Domain Layer
 7 | │  (Business Configuration)   │
 8 | ├─────────────────────────────┤  ↓ depends on
   |                                            ^^
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
   |

invalid-syntax: Got unexpected token │
  --> docs/guides/python-module-organization.md#block5.py:9:1
   |
 7 | │  (Business Configuration)   │
 8 | ├─────────────────────────────┤  ↓ depends on
 9 | │     loader.py               │  # Infrastructure Layer
   | ^
10 | │  (Oracle Data Operations)   │
11 | ├─────────────────────────────┤  ↓ depends on
   |

invalid-syntax: Got unexpected token │
  --> docs/guides/python-module-organization.md#block5.py:9:31
   |
 7 | │  (Business Configuration)   │
 8 | ├─────────────────────────────┤  ↓ depends on
 9 | │     loader.py               │  # Infrastructure Layer
   |                               ^
10 | │  (Oracle Data Operations)   │
11 | ├─────────────────────────────┤  ↓ depends on
   |

invalid-syntax: Expected a statement
  --> docs/guides/python-module-organization.md#block5.py:9:56
   |
 7 | │  (Business Configuration)   │
 8 | ├─────────────────────────────┤  ↓ depends on
 9 | │     loader.py               │  # Infrastructure Layer
   |                                                        ^
10 | │  (Oracle Data Operations)   │
11 | ├─────────────────────────────┤  ↓ depends on
   |

invalid-syntax: Got unexpected token │
  --> docs/guides/python-module-organization.md#block5.py:10:1
   |
 8 | ├─────────────────────────────┤  ↓ depends on
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
   | ^
11 | ├─────────────────────────────┤  ↓ depends on
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
   |

invalid-syntax: Expected `)`, found identifier
  --> docs/guides/python-module-organization.md#block5.py:10:12
   |
 8 | ├─────────────────────────────┤  ↓ depends on
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
   |            ^^^^
11 | ├─────────────────────────────┤  ↓ depends on
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
   |

invalid-syntax: Simple statements must be separated by newlines or semicolons
  --> docs/guides/python-module-organization.md#block5.py:10:17
   |
 8 | ├─────────────────────────────┤  ↓ depends on
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
   |                 ^^^^^^^^^^
11 | ├─────────────────────────────┤  ↓ depends on
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
   |

invalid-syntax: Expected a statement
  --> docs/guides/python-module-organization.md#block5.py:10:27
   |
 8 | ├─────────────────────────────┤  ↓ depends on
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
   |                           ^
11 | ├─────────────────────────────┤  ↓ depends on
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
   |

invalid-syntax: Got unexpected token │
  --> docs/guides/python-module-organization.md#block5.py:10:31
   |
 8 | ├─────────────────────────────┤  ↓ depends on
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
   |                               ^
11 | ├─────────────────────────────┤  ↓ depends on
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
   |

invalid-syntax: Expected a statement
  --> docs/guides/python-module-organization.md#block5.py:10:32
   |
 8 | ├─────────────────────────────┤  ↓ depends on
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
   |                                ^
11 | ├─────────────────────────────┤  ↓ depends on
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
   |

invalid-syntax: Got unexpected token ├
  --> docs/guides/python-module-organization.md#block5.py:11:1
   |
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
11 | ├─────────────────────────────┤  ↓ depends on
   | ^
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:11:2
   |
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
11 | ├─────────────────────────────┤  ↓ depends on
   |  ^
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:11:3
   |
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
11 | ├─────────────────────────────┤  ↓ depends on
   |   ^
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:11:4
   |
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
11 | ├─────────────────────────────┤  ↓ depends on
   |    ^
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:11:5
   |
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
11 | ├─────────────────────────────┤  ↓ depends on
   |     ^
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:11:6
   |
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
11 | ├─────────────────────────────┤  ↓ depends on
   |      ^
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:11:7
   |
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
11 | ├─────────────────────────────┤  ↓ depends on
   |       ^
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:11:8
   |
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
11 | ├─────────────────────────────┤  ↓ depends on
   |        ^
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:11:9
   |
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
11 | ├─────────────────────────────┤  ↓ depends on
   |         ^
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:11:10
   |
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
11 | ├─────────────────────────────┤  ↓ depends on
   |          ^
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:11:11
   |
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
11 | ├─────────────────────────────┤  ↓ depends on
   |           ^
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:11:12
   |
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
11 | ├─────────────────────────────┤  ↓ depends on
   |            ^
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:11:13
   |
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
11 | ├─────────────────────────────┤  ↓ depends on
   |             ^
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:11:14
   |
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
11 | ├─────────────────────────────┤  ↓ depends on
   |              ^
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:11:15
   |
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
11 | ├─────────────────────────────┤  ↓ depends on
   |               ^
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:11:16
   |
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
11 | ├─────────────────────────────┤  ↓ depends on
   |                ^
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:11:17
   |
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
11 | ├─────────────────────────────┤  ↓ depends on
   |                 ^
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:11:18
   |
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
11 | ├─────────────────────────────┤  ↓ depends on
   |                  ^
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:11:19
   |
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
11 | ├─────────────────────────────┤  ↓ depends on
   |                   ^
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:11:20
   |
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
11 | ├─────────────────────────────┤  ↓ depends on
   |                    ^
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:11:21
   |
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
11 | ├─────────────────────────────┤  ↓ depends on
   |                     ^
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:11:22
   |
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
11 | ├─────────────────────────────┤  ↓ depends on
   |                      ^
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:11:23
   |
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
11 | ├─────────────────────────────┤  ↓ depends on
   |                       ^
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:11:24
   |
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
11 | ├─────────────────────────────┤  ↓ depends on
   |                        ^
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:11:25
   |
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
11 | ├─────────────────────────────┤  ↓ depends on
   |                         ^
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:11:26
   |
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
11 | ├─────────────────────────────┤  ↓ depends on
   |                          ^
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:11:27
   |
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
11 | ├─────────────────────────────┤  ↓ depends on
   |                           ^
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:11:28
   |
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
11 | ├─────────────────────────────┤  ↓ depends on
   |                            ^
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:11:29
   |
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
11 | ├─────────────────────────────┤  ↓ depends on
   |                             ^
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:11:30
   |
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
11 | ├─────────────────────────────┤  ↓ depends on
   |                              ^
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
   |

invalid-syntax: Got unexpected token ┤
  --> docs/guides/python-module-organization.md#block5.py:11:31
   |
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
11 | ├─────────────────────────────┤  ↓ depends on
   |                               ^
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
   |

invalid-syntax: Got unexpected token ↓
  --> docs/guides/python-module-organization.md#block5.py:11:34
   |
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
11 | ├─────────────────────────────┤  ↓ depends on
   |                                  ^
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
   |

invalid-syntax: Simple statements must be separated by newlines or semicolons
  --> docs/guides/python-module-organization.md#block5.py:11:44
   |
 9 | │     loader.py               │  # Infrastructure Layer
10 | │  (Oracle Data Operations)   │
11 | ├─────────────────────────────┤  ↓ depends on
   |                                            ^^
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
   |

invalid-syntax: Got unexpected token │
  --> docs/guides/python-module-organization.md#block5.py:12:1
   |
10 | │  (Oracle Data Operations)   │
11 | ├─────────────────────────────┤  ↓ depends on
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
   | ^
13 | │ (r, FlextValueObj)│
14 | └─────────────────────────────┘
   |

invalid-syntax: Simple statements must be separated by newlines or semicolons
  --> docs/guides/python-module-organization.md#block5.py:12:11
   |
10 | │  (Oracle Data Operations)   │
11 | ├─────────────────────────────┤  ↓ depends on
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
   |           ^^^^
13 | │ (r, FlextValueObj)│
14 | └─────────────────────────────┘
   |

invalid-syntax: Simple statements must be separated by newlines or semicolons
  --> docs/guides/python-module-organization.md#block5.py:12:16
   |
10 | │  (Oracle Data Operations)   │
11 | ├─────────────────────────────┤  ↓ depends on
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
   |                ^^^^^^^^^^^^
13 | │ (r, FlextValueObj)│
14 | └─────────────────────────────┘
   |

invalid-syntax: Got unexpected token │
  --> docs/guides/python-module-organization.md#block5.py:12:31
   |
10 | │  (Oracle Data Operations)   │
11 | ├─────────────────────────────┤  ↓ depends on
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
   |                               ^
13 | │ (r, FlextValueObj)│
14 | └─────────────────────────────┘
   |

invalid-syntax: Expected a statement
  --> docs/guides/python-module-organization.md#block5.py:12:52
   |
10 | │  (Oracle Data Operations)   │
11 | ├─────────────────────────────┤  ↓ depends on
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
   |                                                    ^
13 | │ (r, FlextValueObj)│
14 | └─────────────────────────────┘
   |

invalid-syntax: Got unexpected token │
  --> docs/guides/python-module-organization.md#block5.py:13:1
   |
11 | ├─────────────────────────────┤  ↓ depends on
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
   | ^
14 | └─────────────────────────────┘
   |

invalid-syntax: Got unexpected token │
  --> docs/guides/python-module-organization.md#block5.py:13:21
   |
11 | ├─────────────────────────────┤  ↓ depends on
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
   |                     ^
14 | └─────────────────────────────┘
   |

invalid-syntax: Expected a statement
  --> docs/guides/python-module-organization.md#block5.py:13:22
   |
11 | ├─────────────────────────────┤  ↓ depends on
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
   |                      ^
14 | └─────────────────────────────┘
   |

invalid-syntax: Got unexpected token └
  --> docs/guides/python-module-organization.md#block5.py:14:1
   |
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
14 | └─────────────────────────────┘
   | ^
15 |
16 | # Application layer imports
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:14:2
   |
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
14 | └─────────────────────────────┘
   |  ^
15 |
16 | # Application layer imports
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:14:3
   |
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
14 | └─────────────────────────────┘
   |   ^
15 |
16 | # Application layer imports
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:14:4
   |
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
14 | └─────────────────────────────┘
   |    ^
15 |
16 | # Application layer imports
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:14:5
   |
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
14 | └─────────────────────────────┘
   |     ^
15 |
16 | # Application layer imports
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:14:6
   |
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
14 | └─────────────────────────────┘
   |      ^
15 |
16 | # Application layer imports
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:14:7
   |
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
14 | └─────────────────────────────┘
   |       ^
15 |
16 | # Application layer imports
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:14:8
   |
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
14 | └─────────────────────────────┘
   |        ^
15 |
16 | # Application layer imports
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:14:9
   |
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
14 | └─────────────────────────────┘
   |         ^
15 |
16 | # Application layer imports
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:14:10
   |
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
14 | └─────────────────────────────┘
   |          ^
15 |
16 | # Application layer imports
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:14:11
   |
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
14 | └─────────────────────────────┘
   |           ^
15 |
16 | # Application layer imports
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:14:12
   |
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
14 | └─────────────────────────────┘
   |            ^
15 |
16 | # Application layer imports
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:14:13
   |
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
14 | └─────────────────────────────┘
   |             ^
15 |
16 | # Application layer imports
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:14:14
   |
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
14 | └─────────────────────────────┘
   |              ^
15 |
16 | # Application layer imports
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:14:15
   |
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
14 | └─────────────────────────────┘
   |               ^
15 |
16 | # Application layer imports
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:14:16
   |
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
14 | └─────────────────────────────┘
   |                ^
15 |
16 | # Application layer imports
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:14:17
   |
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
14 | └─────────────────────────────┘
   |                 ^
15 |
16 | # Application layer imports
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:14:18
   |
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
14 | └─────────────────────────────┘
   |                  ^
15 |
16 | # Application layer imports
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:14:19
   |
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
14 | └─────────────────────────────┘
   |                   ^
15 |
16 | # Application layer imports
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:14:20
   |
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
14 | └─────────────────────────────┘
   |                    ^
15 |
16 | # Application layer imports
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:14:21
   |
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
14 | └─────────────────────────────┘
   |                     ^
15 |
16 | # Application layer imports
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:14:22
   |
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
14 | └─────────────────────────────┘
   |                      ^
15 |
16 | # Application layer imports
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:14:23
   |
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
14 | └─────────────────────────────┘
   |                       ^
15 |
16 | # Application layer imports
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:14:24
   |
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
14 | └─────────────────────────────┘
   |                        ^
15 |
16 | # Application layer imports
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:14:25
   |
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
14 | └─────────────────────────────┘
   |                         ^
15 |
16 | # Application layer imports
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:14:26
   |
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
14 | └─────────────────────────────┘
   |                          ^
15 |
16 | # Application layer imports
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:14:27
   |
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
14 | └─────────────────────────────┘
   |                           ^
15 |
16 | # Application layer imports
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:14:28
   |
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
14 | └─────────────────────────────┘
   |                            ^
15 |
16 | # Application layer imports
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:14:29
   |
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
14 | └─────────────────────────────┘
   |                             ^
15 |
16 | # Application layer imports
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block5.py:14:30
   |
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
14 | └─────────────────────────────┘
   |                              ^
15 |
16 | # Application layer imports
   |

invalid-syntax: Got unexpected token ┘
  --> docs/guides/python-module-organization.md#block5.py:14:31
   |
12 | │   FLEXT Core Dependencies   │  # Foundation Layer
13 | │ (r, FlextValueObj)│
14 | └─────────────────────────────┘
   |                               ^
15 |
16 | # Application layer imports
   |

Found 194 errors. |
| docs/guides/python-module-organization.md | python_codeblock | medium | block #6: invalid-syntax: Expected `,`, found `.`
 --> docs/guides/python-module-organization.md#block6.py:6:23
  |
4 | from flext_meltano import Target  # Singer SDK integration layer
5 | from flext_db_oracle import FlextDbOracleApi, FlextDbOracleSettings
6 | from pydantic import u.Field, m.field_validator  # Third-party validation
  |                       ^
7 |
8 | # ✅ CORRECT - Standard library imports
  |

invalid-syntax: Expected `,`, found `.`
 --> docs/guides/python-module-organization.md#block6.py:6:32
  |
4 | from flext_meltano import Target  # Singer SDK integration layer
5 | from flext_db_oracle import FlextDbOracleApi, FlextDbOracleSettings
6 | from pydantic import u.Field, m.field_validator  # Third-party validation
  |                                ^
7 |
8 | # ✅ CORRECT - Standard library imports
  |

Found 2 errors. |
| docs/guides/python-module-organization.md | python_codeblock | medium | block #7: missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
 --> docs/guides/python-module-organization.md#block7.py:1:6
  |
1 | tests/
  |      ^
2 | ├── unit/                           # Unit tests (isolated)
3 | │   ├── test_config.py             # Tests settings.py
  |
help: Add missing whitespace

invalid-syntax: Expected an expression
 --> docs/guides/python-module-organization.md#block7.py:1:7
  |
1 | tests/
  |       ^
2 | ├── unit/                           # Unit tests (isolated)
3 | │   ├── test_config.py             # Tests settings.py
  |

invalid-syntax: Got unexpected token ├
 --> docs/guides/python-module-organization.md#block7.py:2:1
  |
1 | tests/
2 | ├── unit/                           # Unit tests (isolated)
  | ^
3 | │   ├── test_config.py             # Tests settings.py
4 | │   ├── test_target.py             # Tests target.py
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block7.py:2:2
  |
1 | tests/
2 | ├── unit/                           # Unit tests (isolated)
  |  ^
3 | │   ├── test_config.py             # Tests settings.py
4 | │   ├── test_target.py             # Tests target.py
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block7.py:2:3
  |
1 | tests/
2 | ├── unit/                           # Unit tests (isolated)
  |   ^
3 | │   ├── test_config.py             # Tests settings.py
4 | │   ├── test_target.py             # Tests target.py
  |

missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
 --> docs/guides/python-module-organization.md#block7.py:2:9
  |
1 | tests/
2 | ├── unit/                           # Unit tests (isolated)
  |         ^
3 | │   ├── test_config.py             # Tests settings.py
4 | │   ├── test_target.py             # Tests target.py
  |
help: Add missing whitespace

invalid-syntax: Expected an expression
 --> docs/guides/python-module-organization.md#block7.py:2:60
  |
1 | tests/
2 | ├── unit/                           # Unit tests (isolated)
  |                                                            ^
3 | │   ├── test_config.py             # Tests settings.py
4 | │   ├── test_target.py             # Tests target.py
  |

invalid-syntax: Got unexpected token │
 --> docs/guides/python-module-organization.md#block7.py:3:1
  |
1 | tests/
2 | ├── unit/                           # Unit tests (isolated)
3 | │   ├── test_config.py             # Tests settings.py
  | ^
4 | │   ├── test_target.py             # Tests target.py
5 | │   ├── test_loader.py             # Tests loader.py
  |

invalid-syntax: Got unexpected token ├
 --> docs/guides/python-module-organization.md#block7.py:3:5
  |
1 | tests/
2 | ├── unit/                           # Unit tests (isolated)
3 | │   ├── test_config.py             # Tests settings.py
  |     ^
4 | │   ├── test_target.py             # Tests target.py
5 | │   ├── test_loader.py             # Tests loader.py
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block7.py:3:6
  |
1 | tests/
2 | ├── unit/                           # Unit tests (isolated)
3 | │   ├── test_config.py             # Tests settings.py
  |      ^
4 | │   ├── test_target.py             # Tests target.py
5 | │   ├── test_loader.py             # Tests loader.py
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block7.py:3:7
  |
1 | tests/
2 | ├── unit/                           # Unit tests (isolated)
3 | │   ├── test_config.py             # Tests settings.py
  |       ^
4 | │   ├── test_target.py             # Tests target.py
5 | │   ├── test_loader.py             # Tests loader.py
  |

invalid-syntax: Got unexpected token │
 --> docs/guides/python-module-organization.md#block7.py:4:1
  |
2 | ├── unit/                           # Unit tests (isolated)
3 | │   ├── test_config.py             # Tests settings.py
4 | │   ├── test_target.py             # Tests target.py
  | ^
5 | │   ├── test_loader.py             # Tests loader.py
6 | │   └── test_exceptions.py         # Tests exceptions.py
  |

invalid-syntax: Got unexpected token ├
 --> docs/guides/python-module-organization.md#block7.py:4:5
  |
2 | ├── unit/                           # Unit tests (isolated)
3 | │   ├── test_config.py             # Tests settings.py
4 | │   ├── test_target.py             # Tests target.py
  |     ^
5 | │   ├── test_loader.py             # Tests loader.py
6 | │   └── test_exceptions.py         # Tests exceptions.py
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block7.py:4:6
  |
2 | ├── unit/                           # Unit tests (isolated)
3 | │   ├── test_config.py             # Tests settings.py
4 | │   ├── test_target.py             # Tests target.py
  |      ^
5 | │   ├── test_loader.py             # Tests loader.py
6 | │   └── test_exceptions.py         # Tests exceptions.py
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block7.py:4:7
  |
2 | ├── unit/                           # Unit tests (isolated)
3 | │   ├── test_config.py             # Tests settings.py
4 | │   ├── test_target.py             # Tests target.py
  |       ^
5 | │   ├── test_loader.py             # Tests loader.py
6 | │   └── test_exceptions.py         # Tests exceptions.py
  |

invalid-syntax: Got unexpected token │
 --> docs/guides/python-module-organization.md#block7.py:5:1
  |
3 | │   ├── test_config.py             # Tests settings.py
4 | │   ├── test_target.py             # Tests target.py
5 | │   ├── test_loader.py             # Tests loader.py
  | ^
6 | │   └── test_exceptions.py         # Tests exceptions.py
7 | ├── integration/                   # Integration tests
  |

invalid-syntax: Got unexpected token ├
 --> docs/guides/python-module-organization.md#block7.py:5:5
  |
3 | │   ├── test_config.py             # Tests settings.py
4 | │   ├── test_target.py             # Tests target.py
5 | │   ├── test_loader.py             # Tests loader.py
  |     ^
6 | │   └── test_exceptions.py         # Tests exceptions.py
7 | ├── integration/                   # Integration tests
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block7.py:5:6
  |
3 | │   ├── test_config.py             # Tests settings.py
4 | │   ├── test_target.py             # Tests target.py
5 | │   ├── test_loader.py             # Tests loader.py
  |      ^
6 | │   └── test_exceptions.py         # Tests exceptions.py
7 | ├── integration/                   # Integration tests
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block7.py:5:7
  |
3 | │   ├── test_config.py             # Tests settings.py
4 | │   ├── test_target.py             # Tests target.py
5 | │   ├── test_loader.py             # Tests loader.py
  |       ^
6 | │   └── test_exceptions.py         # Tests exceptions.py
7 | ├── integration/                   # Integration tests
  |

invalid-syntax: Got unexpected token │
 --> docs/guides/python-module-organization.md#block7.py:6:1
  |
4 | │   ├── test_target.py             # Tests target.py
5 | │   ├── test_loader.py             # Tests loader.py
6 | │   └── test_exceptions.py         # Tests exceptions.py
  | ^
7 | ├── integration/                   # Integration tests
8 | │   ├── test_oracle_connection.py  # Oracle database integration
  |

invalid-syntax: Got unexpected token └
 --> docs/guides/python-module-organization.md#block7.py:6:5
  |
4 | │   ├── test_target.py             # Tests target.py
5 | │   ├── test_loader.py             # Tests loader.py
6 | │   └── test_exceptions.py         # Tests exceptions.py
  |     ^
7 | ├── integration/                   # Integration tests
8 | │   ├── test_oracle_connection.py  # Oracle database integration
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block7.py:6:6
  |
4 | │   ├── test_target.py             # Tests target.py
5 | │   ├── test_loader.py             # Tests loader.py
6 | │   └── test_exceptions.py         # Tests exceptions.py
  |      ^
7 | ├── integration/                   # Integration tests
8 | │   ├── test_oracle_connection.py  # Oracle database integration
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block7.py:6:7
  |
4 | │   ├── test_target.py             # Tests target.py
5 | │   ├── test_loader.py             # Tests loader.py
6 | │   └── test_exceptions.py         # Tests exceptions.py
  |       ^
7 | ├── integration/                   # Integration tests
8 | │   ├── test_oracle_connection.py  # Oracle database integration
  |

invalid-syntax: Got unexpected token ├
 --> docs/guides/python-module-organization.md#block7.py:7:1
  |
5 | │   ├── test_loader.py             # Tests loader.py
6 | │   └── test_exceptions.py         # Tests exceptions.py
7 | ├── integration/                   # Integration tests
  | ^
8 | │   ├── test_oracle_connection.py  # Oracle database integration
9 | │   ├── test_singer_compliance.py  # Singer protocol compliance
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block7.py:7:2
  |
5 | │   ├── test_loader.py             # Tests loader.py
6 | │   └── test_exceptions.py         # Tests exceptions.py
7 | ├── integration/                   # Integration tests
  |  ^
8 | │   ├── test_oracle_connection.py  # Oracle database integration
9 | │   ├── test_singer_compliance.py  # Singer protocol compliance
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block7.py:7:3
  |
5 | │   ├── test_loader.py             # Tests loader.py
6 | │   └── test_exceptions.py         # Tests exceptions.py
7 | ├── integration/                   # Integration tests
  |   ^
8 | │   ├── test_oracle_connection.py  # Oracle database integration
9 | │   ├── test_singer_compliance.py  # Singer protocol compliance
  |

missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
 --> docs/guides/python-module-organization.md#block7.py:7:16
  |
5 | │   ├── test_loader.py             # Tests loader.py
6 | │   └── test_exceptions.py         # Tests exceptions.py
7 | ├── integration/                   # Integration tests
  |                ^
8 | │   ├── test_oracle_connection.py  # Oracle database integration
9 | │   ├── test_singer_compliance.py  # Singer protocol compliance
  |
help: Add missing whitespace

invalid-syntax: Expected an expression
 --> docs/guides/python-module-organization.md#block7.py:7:55
  |
5 | │   ├── test_loader.py             # Tests loader.py
6 | │   └── test_exceptions.py         # Tests exceptions.py
7 | ├── integration/                   # Integration tests
  |                                                       ^
8 | │   ├── test_oracle_connection.py  # Oracle database integration
9 | │   ├── test_singer_compliance.py  # Singer protocol compliance
  |

invalid-syntax: Got unexpected token │
  --> docs/guides/python-module-organization.md#block7.py:8:1
   |
 6 | │   └── test_exceptions.py         # Tests exceptions.py
 7 | ├── integration/                   # Integration tests
 8 | │   ├── test_oracle_connection.py  # Oracle database integration
   | ^
 9 | │   ├── test_singer_compliance.py  # Singer protocol compliance
10 | │   └── test_end_to_end.py         # Complete workflow tests
   |

invalid-syntax: Got unexpected token ├
  --> docs/guides/python-module-organization.md#block7.py:8:5
   |
 6 | │   └── test_exceptions.py         # Tests exceptions.py
 7 | ├── integration/                   # Integration tests
 8 | │   ├── test_oracle_connection.py  # Oracle database integration
   |     ^
 9 | │   ├── test_singer_compliance.py  # Singer protocol compliance
10 | │   └── test_end_to_end.py         # Complete workflow tests
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block7.py:8:6
   |
 6 | │   └── test_exceptions.py         # Tests exceptions.py
 7 | ├── integration/                   # Integration tests
 8 | │   ├── test_oracle_connection.py  # Oracle database integration
   |      ^
 9 | │   ├── test_singer_compliance.py  # Singer protocol compliance
10 | │   └── test_end_to_end.py         # Complete workflow tests
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block7.py:8:7
   |
 6 | │   └── test_exceptions.py         # Tests exceptions.py
 7 | ├── integration/                   # Integration tests
 8 | │   ├── test_oracle_connection.py  # Oracle database integration
   |       ^
 9 | │   ├── test_singer_compliance.py  # Singer protocol compliance
10 | │   └── test_end_to_end.py         # Complete workflow tests
   |

invalid-syntax: Got unexpected token │
  --> docs/guides/python-module-organization.md#block7.py:9:1
   |
 7 | ├── integration/                   # Integration tests
 8 | │   ├── test_oracle_connection.py  # Oracle database integration
 9 | │   ├── test_singer_compliance.py  # Singer protocol compliance
   | ^
10 | │   └── test_end_to_end.py         # Complete workflow tests
11 | ├── performance/                   # Performance tests
   |

invalid-syntax: Got unexpected token ├
  --> docs/guides/python-module-organization.md#block7.py:9:5
   |
 7 | ├── integration/                   # Integration tests
 8 | │   ├── test_oracle_connection.py  # Oracle database integration
 9 | │   ├── test_singer_compliance.py  # Singer protocol compliance
   |     ^
10 | │   └── test_end_to_end.py         # Complete workflow tests
11 | ├── performance/                   # Performance tests
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block7.py:9:6
   |
 7 | ├── integration/                   # Integration tests
 8 | │   ├── test_oracle_connection.py  # Oracle database integration
 9 | │   ├── test_singer_compliance.py  # Singer protocol compliance
   |      ^
10 | │   └── test_end_to_end.py         # Complete workflow tests
11 | ├── performance/                   # Performance tests
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block7.py:9:7
   |
 7 | ├── integration/                   # Integration tests
 8 | │   ├── test_oracle_connection.py  # Oracle database integration
 9 | │   ├── test_singer_compliance.py  # Singer protocol compliance
   |       ^
10 | │   └── test_end_to_end.py         # Complete workflow tests
11 | ├── performance/                   # Performance tests
   |

invalid-syntax: Got unexpected token │
  --> docs/guides/python-module-organization.md#block7.py:10:1
   |
 8 | │   ├── test_oracle_connection.py  # Oracle database integration
 9 | │   ├── test_singer_compliance.py  # Singer protocol compliance
10 | │   └── test_end_to_end.py         # Complete workflow tests
   | ^
11 | ├── performance/                   # Performance tests
12 | │   ├── test_batch_performance.py  # Batch processing benchmarks
   |

invalid-syntax: Got unexpected token └
  --> docs/guides/python-module-organization.md#block7.py:10:5
   |
 8 | │   ├── test_oracle_connection.py  # Oracle database integration
 9 | │   ├── test_singer_compliance.py  # Singer protocol compliance
10 | │   └── test_end_to_end.py         # Complete workflow tests
   |     ^
11 | ├── performance/                   # Performance tests
12 | │   ├── test_batch_performance.py  # Batch processing benchmarks
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block7.py:10:6
   |
 8 | │   ├── test_oracle_connection.py  # Oracle database integration
 9 | │   ├── test_singer_compliance.py  # Singer protocol compliance
10 | │   └── test_end_to_end.py         # Complete workflow tests
   |      ^
11 | ├── performance/                   # Performance tests
12 | │   ├── test_batch_performance.py  # Batch processing benchmarks
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block7.py:10:7
   |
 8 | │   ├── test_oracle_connection.py  # Oracle database integration
 9 | │   ├── test_singer_compliance.py  # Singer protocol compliance
10 | │   └── test_end_to_end.py         # Complete workflow tests
   |       ^
11 | ├── performance/                   # Performance tests
12 | │   ├── test_batch_performance.py  # Batch processing benchmarks
   |

invalid-syntax: Got unexpected token ├
  --> docs/guides/python-module-organization.md#block7.py:11:1
   |
 9 | │   ├── test_singer_compliance.py  # Singer protocol compliance
10 | │   └── test_end_to_end.py         # Complete workflow tests
11 | ├── performance/                   # Performance tests
   | ^
12 | │   ├── test_batch_performance.py  # Batch processing benchmarks
13 | │   └── test_connection_pooling.py # Connection performance
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block7.py:11:2
   |
 9 | │   ├── test_singer_compliance.py  # Singer protocol compliance
10 | │   └── test_end_to_end.py         # Complete workflow tests
11 | ├── performance/                   # Performance tests
   |  ^
12 | │   ├── test_batch_performance.py  # Batch processing benchmarks
13 | │   └── test_connection_pooling.py # Connection performance
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block7.py:11:3
   |
 9 | │   ├── test_singer_compliance.py  # Singer protocol compliance
10 | │   └── test_end_to_end.py         # Complete workflow tests
11 | ├── performance/                   # Performance tests
   |   ^
12 | │   ├── test_batch_performance.py  # Batch processing benchmarks
13 | │   └── test_connection_pooling.py # Connection performance
   |

missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
  --> docs/guides/python-module-organization.md#block7.py:11:16
   |
 9 | │   ├── test_singer_compliance.py  # Singer protocol compliance
10 | │   └── test_end_to_end.py         # Complete workflow tests
11 | ├── performance/                   # Performance tests
   |                ^
12 | │   ├── test_batch_performance.py  # Batch processing benchmarks
13 | │   └── test_connection_pooling.py # Connection performance
   |
help: Add missing whitespace

invalid-syntax: Expected an expression
  --> docs/guides/python-module-organization.md#block7.py:11:55
   |
 9 | │   ├── test_singer_compliance.py  # Singer protocol compliance
10 | │   └── test_end_to_end.py         # Complete workflow tests
11 | ├── performance/                   # Performance tests
   |                                                       ^
12 | │   ├── test_batch_performance.py  # Batch processing benchmarks
13 | │   └── test_connection_pooling.py # Connection performance
   |

invalid-syntax: Got unexpected token │
  --> docs/guides/python-module-organization.md#block7.py:12:1
   |
10 | │   └── test_end_to_end.py         # Complete workflow tests
11 | ├── performance/                   # Performance tests
12 | │   ├── test_batch_performance.py  # Batch processing benchmarks
   | ^
13 | │   └── test_connection_pooling.py # Connection performance
14 | ├── security/                      # Security tests
   |

invalid-syntax: Got unexpected token ├
  --> docs/guides/python-module-organization.md#block7.py:12:5
   |
10 | │   └── test_end_to_end.py         # Complete workflow tests
11 | ├── performance/                   # Performance tests
12 | │   ├── test_batch_performance.py  # Batch processing benchmarks
   |     ^
13 | │   └── test_connection_pooling.py # Connection performance
14 | ├── security/                      # Security tests
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block7.py:12:6
   |
10 | │   └── test_end_to_end.py         # Complete workflow tests
11 | ├── performance/                   # Performance tests
12 | │   ├── test_batch_performance.py  # Batch processing benchmarks
   |      ^
13 | │   └── test_connection_pooling.py # Connection performance
14 | ├── security/                      # Security tests
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block7.py:12:7
   |
10 | │   └── test_end_to_end.py         # Complete workflow tests
11 | ├── performance/                   # Performance tests
12 | │   ├── test_batch_performance.py  # Batch processing benchmarks
   |       ^
13 | │   └── test_connection_pooling.py # Connection performance
14 | ├── security/                      # Security tests
   |

invalid-syntax: Got unexpected token │
  --> docs/guides/python-module-organization.md#block7.py:13:1
   |
11 | ├── performance/                   # Performance tests
12 | │   ├── test_batch_performance.py  # Batch processing benchmarks
13 | │   └── test_connection_pooling.py # Connection performance
   | ^
14 | ├── security/                      # Security tests
15 | │   ├── test_sql_injection.py      # SQL injection prevention
   |

invalid-syntax: Got unexpected token └
  --> docs/guides/python-module-organization.md#block7.py:13:5
   |
11 | ├── performance/                   # Performance tests
12 | │   ├── test_batch_performance.py  # Batch processing benchmarks
13 | │   └── test_connection_pooling.py # Connection performance
   |     ^
14 | ├── security/                      # Security tests
15 | │   ├── test_sql_injection.py      # SQL injection prevention
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block7.py:13:6
   |
11 | ├── performance/                   # Performance tests
12 | │   ├── test_batch_performance.py  # Batch processing benchmarks
13 | │   └── test_connection_pooling.py # Connection performance
   |      ^
14 | ├── security/                      # Security tests
15 | │   ├── test_sql_injection.py      # SQL injection prevention
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block7.py:13:7
   |
11 | ├── performance/                   # Performance tests
12 | │   ├── test_batch_performance.py  # Batch processing benchmarks
13 | │   └── test_connection_pooling.py # Connection performance
   |       ^
14 | ├── security/                      # Security tests
15 | │   ├── test_sql_injection.py      # SQL injection prevention
   |

too-few-spaces-before-inline-comment: Insert at least two spaces before an inline comment
  --> docs/guides/python-module-organization.md#block7.py:13:35
   |
11 | ├── performance/                   # Performance tests
12 | │   ├── test_batch_performance.py  # Batch processing benchmarks
13 | │   └── test_connection_pooling.py # Connection performance
   |                                   ^
14 | ├── security/                      # Security tests
15 | │   ├── test_sql_injection.py      # SQL injection prevention
   |
help: Insert spaces

invalid-syntax: Got unexpected token ├
  --> docs/guides/python-module-organization.md#block7.py:14:1
   |
12 | │   ├── test_batch_performance.py  # Batch processing benchmarks
13 | │   └── test_connection_pooling.py # Connection performance
14 | ├── security/                      # Security tests
   | ^
15 | │   ├── test_sql_injection.py      # SQL injection prevention
16 | │   └── test_credential_handling.py # Credential security
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block7.py:14:2
   |
12 | │   ├── test_batch_performance.py  # Batch processing benchmarks
13 | │   └── test_connection_pooling.py # Connection performance
14 | ├── security/                      # Security tests
   |  ^
15 | │   ├── test_sql_injection.py      # SQL injection prevention
16 | │   └── test_credential_handling.py # Credential security
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block7.py:14:3
   |
12 | │   ├── test_batch_performance.py  # Batch processing benchmarks
13 | │   └── test_connection_pooling.py # Connection performance
14 | ├── security/                      # Security tests
   |   ^
15 | │   ├── test_sql_injection.py      # SQL injection prevention
16 | │   └── test_credential_handling.py # Credential security
   |

missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
  --> docs/guides/python-module-organization.md#block7.py:14:13
   |
12 | │   ├── test_batch_performance.py  # Batch processing benchmarks
13 | │   └── test_connection_pooling.py # Connection performance
14 | ├── security/                      # Security tests
   |             ^
15 | │   ├── test_sql_injection.py      # SQL injection prevention
16 | │   └── test_credential_handling.py # Credential security
   |
help: Add missing whitespace

invalid-syntax: Expected an expression
  --> docs/guides/python-module-organization.md#block7.py:14:52
   |
12 | │   ├── test_batch_performance.py  # Batch processing benchmarks
13 | │   └── test_connection_pooling.py # Connection performance
14 | ├── security/                      # Security tests
   |                                                    ^
15 | │   ├── test_sql_injection.py      # SQL injection prevention
16 | │   └── test_credential_handling.py # Credential security
   |

invalid-syntax: Got unexpected token │
  --> docs/guides/python-module-organization.md#block7.py:15:1
   |
13 | │   └── test_connection_pooling.py # Connection performance
14 | ├── security/                      # Security tests
15 | │   ├── test_sql_injection.py      # SQL injection prevention
   | ^
16 | │   └── test_credential_handling.py # Credential security
17 | ├── conftest.py                    # Test configuration & fixtures
   |

invalid-syntax: Got unexpected token ├
  --> docs/guides/python-module-organization.md#block7.py:15:5
   |
13 | │   └── test_connection_pooling.py # Connection performance
14 | ├── security/                      # Security tests
15 | │   ├── test_sql_injection.py      # SQL injection prevention
   |     ^
16 | │   └── test_credential_handling.py # Credential security
17 | ├── conftest.py                    # Test configuration & fixtures
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block7.py:15:6
   |
13 | │   └── test_connection_pooling.py # Connection performance
14 | ├── security/                      # Security tests
15 | │   ├── test_sql_injection.py      # SQL injection prevention
   |      ^
16 | │   └── test_credential_handling.py # Credential security
17 | ├── conftest.py                    # Test configuration & fixtures
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block7.py:15:7
   |
13 | │   └── test_connection_pooling.py # Connection performance
14 | ├── security/                      # Security tests
15 | │   ├── test_sql_injection.py      # SQL injection prevention
   |       ^
16 | │   └── test_credential_handling.py # Credential security
17 | ├── conftest.py                    # Test configuration & fixtures
   |

invalid-syntax: Got unexpected token │
  --> docs/guides/python-module-organization.md#block7.py:16:1
   |
14 | ├── security/                      # Security tests
15 | │   ├── test_sql_injection.py      # SQL injection prevention
16 | │   └── test_credential_handling.py # Credential security
   | ^
17 | ├── conftest.py                    # Test configuration & fixtures
18 | └── fixtures/                      # Test data and setup
   |

invalid-syntax: Got unexpected token └
  --> docs/guides/python-module-organization.md#block7.py:16:5
   |
14 | ├── security/                      # Security tests
15 | │   ├── test_sql_injection.py      # SQL injection prevention
16 | │   └── test_credential_handling.py # Credential security
   |     ^
17 | ├── conftest.py                    # Test configuration & fixtures
18 | └── fixtures/                      # Test data and setup
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block7.py:16:6
   |
14 | ├── security/                      # Security tests
15 | │   ├── test_sql_injection.py      # SQL injection prevention
16 | │   └── test_credential_handling.py # Credential security
   |      ^
17 | ├── conftest.py                    # Test configuration & fixtures
18 | └── fixtures/                      # Test data and setup
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block7.py:16:7
   |
14 | ├── security/                      # Security tests
15 | │   ├── test_sql_injection.py      # SQL injection prevention
16 | │   └── test_credential_handling.py # Credential security
   |       ^
17 | ├── conftest.py                    # Test configuration & fixtures
18 | └── fixtures/                      # Test data and setup
   |

too-few-spaces-before-inline-comment: Insert at least two spaces before an inline comment
  --> docs/guides/python-module-organization.md#block7.py:16:36
   |
14 | ├── security/                      # Security tests
15 | │   ├── test_sql_injection.py      # SQL injection prevention
16 | │   └── test_credential_handling.py # Credential security
   |                                    ^
17 | ├── conftest.py                    # Test configuration & fixtures
18 | └── fixtures/                      # Test data and setup
   |
help: Insert spaces

invalid-syntax: Got unexpected token ├
  --> docs/guides/python-module-organization.md#block7.py:17:1
   |
15 | │   ├── test_sql_injection.py      # SQL injection prevention
16 | │   └── test_credential_handling.py # Credential security
17 | ├── conftest.py                    # Test configuration & fixtures
   | ^
18 | └── fixtures/                      # Test data and setup
19 |     ├── oracle_schemas.py          # Test schema definitions
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block7.py:17:2
   |
15 | │   ├── test_sql_injection.py      # SQL injection prevention
16 | │   └── test_credential_handling.py # Credential security
17 | ├── conftest.py                    # Test configuration & fixtures
   |  ^
18 | └── fixtures/                      # Test data and setup
19 |     ├── oracle_schemas.py          # Test schema definitions
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block7.py:17:3
   |
15 | │   ├── test_sql_injection.py      # SQL injection prevention
16 | │   └── test_credential_handling.py # Credential security
17 | ├── conftest.py                    # Test configuration & fixtures
   |   ^
18 | └── fixtures/                      # Test data and setup
19 |     ├── oracle_schemas.py          # Test schema definitions
   |

invalid-syntax: Got unexpected token └
  --> docs/guides/python-module-organization.md#block7.py:18:1
   |
16 | │   └── test_credential_handling.py # Credential security
17 | ├── conftest.py                    # Test configuration & fixtures
18 | └── fixtures/                      # Test data and setup
   | ^
19 |     ├── oracle_schemas.py          # Test schema definitions
20 |     ├── singer_messages.py         # Sample Singer messages
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block7.py:18:2
   |
16 | │   └── test_credential_handling.py # Credential security
17 | ├── conftest.py                    # Test configuration & fixtures
18 | └── fixtures/                      # Test data and setup
   |  ^
19 |     ├── oracle_schemas.py          # Test schema definitions
20 |     ├── singer_messages.py         # Sample Singer messages
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block7.py:18:3
   |
16 | │   └── test_credential_handling.py # Credential security
17 | ├── conftest.py                    # Test configuration & fixtures
18 | └── fixtures/                      # Test data and setup
   |   ^
19 |     ├── oracle_schemas.py          # Test schema definitions
20 |     ├── singer_messages.py         # Sample Singer messages
   |

missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
  --> docs/guides/python-module-organization.md#block7.py:18:13
   |
16 | │   └── test_credential_handling.py # Credential security
17 | ├── conftest.py                    # Test configuration & fixtures
18 | └── fixtures/                      # Test data and setup
   |             ^
19 |     ├── oracle_schemas.py          # Test schema definitions
20 |     ├── singer_messages.py         # Sample Singer messages
   |
help: Add missing whitespace

invalid-syntax: Expected an expression
  --> docs/guides/python-module-organization.md#block7.py:18:57
   |
16 | │   └── test_credential_handling.py # Credential security
17 | ├── conftest.py                    # Test configuration & fixtures
18 | └── fixtures/                      # Test data and setup
   |                                                         ^
19 |     ├── oracle_schemas.py          # Test schema definitions
20 |     ├── singer_messages.py         # Sample Singer messages
   |

invalid-syntax: Unexpected indentation
  --> docs/guides/python-module-organization.md#block7.py:19:1
   |
17 | ├── conftest.py                    # Test configuration & fixtures
18 | └── fixtures/                      # Test data and setup
19 |     ├── oracle_schemas.py          # Test schema definitions
   | ^^^^
20 |     ├── singer_messages.py         # Sample Singer messages
21 |     └── test_data.py               # Test datasets
   |

unexpected-indentation: Unexpected indentation
  --> docs/guides/python-module-organization.md#block7.py:19:1
   |
17 | ├── conftest.py                    # Test configuration & fixtures
18 | └── fixtures/                      # Test data and setup
19 |     ├── oracle_schemas.py          # Test schema definitions
   | ^^^^
20 |     ├── singer_messages.py         # Sample Singer messages
21 |     └── test_data.py               # Test datasets
   |

invalid-syntax: Got unexpected token ├
  --> docs/guides/python-module-organization.md#block7.py:19:5
   |
17 | ├── conftest.py                    # Test configuration & fixtures
18 | └── fixtures/                      # Test data and setup
19 |     ├── oracle_schemas.py          # Test schema definitions
   |     ^
20 |     ├── singer_messages.py         # Sample Singer messages
21 |     └── test_data.py               # Test datasets
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block7.py:19:6
   |
17 | ├── conftest.py                    # Test configuration & fixtures
18 | └── fixtures/                      # Test data and setup
19 |     ├── oracle_schemas.py          # Test schema definitions
   |      ^
20 |     ├── singer_messages.py         # Sample Singer messages
21 |     └── test_data.py               # Test datasets
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block7.py:19:7
   |
17 | ├── conftest.py                    # Test configuration & fixtures
18 | └── fixtures/                      # Test data and setup
19 |     ├── oracle_schemas.py          # Test schema definitions
   |       ^
20 |     ├── singer_messages.py         # Sample Singer messages
21 |     └── test_data.py               # Test datasets
   |

invalid-syntax: Got unexpected token ├
  --> docs/guides/python-module-organization.md#block7.py:20:5
   |
18 | └── fixtures/                      # Test data and setup
19 |     ├── oracle_schemas.py          # Test schema definitions
20 |     ├── singer_messages.py         # Sample Singer messages
   |     ^
21 |     └── test_data.py               # Test datasets
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block7.py:20:6
   |
18 | └── fixtures/                      # Test data and setup
19 |     ├── oracle_schemas.py          # Test schema definitions
20 |     ├── singer_messages.py         # Sample Singer messages
   |      ^
21 |     └── test_data.py               # Test datasets
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block7.py:20:7
   |
18 | └── fixtures/                      # Test data and setup
19 |     ├── oracle_schemas.py          # Test schema definitions
20 |     ├── singer_messages.py         # Sample Singer messages
   |       ^
21 |     └── test_data.py               # Test datasets
   |

invalid-syntax: Got unexpected token └
  --> docs/guides/python-module-organization.md#block7.py:21:5
   |
19 |     ├── oracle_schemas.py          # Test schema definitions
20 |     ├── singer_messages.py         # Sample Singer messages
21 |     └── test_data.py               # Test datasets
   |     ^

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block7.py:21:6
   |
19 |     ├── oracle_schemas.py          # Test schema definitions
20 |     ├── singer_messages.py         # Sample Singer messages
21 |     └── test_data.py               # Test datasets
   |      ^

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block7.py:21:7
   |
19 |     ├── oracle_schemas.py          # Test schema definitions
20 |     ├── singer_messages.py         # Sample Singer messages
21 |     └── test_data.py               # Test datasets
   |       ^

Found 87 errors. |
| docs/guides/python-module-organization.md | python_codeblock | medium | block #8: missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
 --> docs/guides/python-module-organization.md#block8.py:1:4
  |
1 | src/flext_target_oracle/
  |    ^
2 | ├── settings/
3 | │   ├── environments.py     # Environment-specific configurations
  |
help: Add missing whitespace

missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
 --> docs/guides/python-module-organization.md#block8.py:1:24
  |
1 | src/flext_target_oracle/
  |                        ^
2 | ├── settings/
3 | │   ├── environments.py     # Environment-specific configurations
  |
help: Add missing whitespace

invalid-syntax: Expected an expression
 --> docs/guides/python-module-organization.md#block8.py:1:25
  |
1 | src/flext_target_oracle/
  |                         ^
2 | ├── settings/
3 | │   ├── environments.py     # Environment-specific configurations
  |

invalid-syntax: Got unexpected token ├
 --> docs/guides/python-module-organization.md#block8.py:2:1
  |
1 | src/flext_target_oracle/
2 | ├── settings/
  | ^
3 | │   ├── environments.py     # Environment-specific configurations
4 | │   ├── schema_evolution.py # Table modification strategies
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block8.py:2:2
  |
1 | src/flext_target_oracle/
2 | ├── settings/
  |  ^
3 | │   ├── environments.py     # Environment-specific configurations
4 | │   ├── schema_evolution.py # Table modification strategies
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block8.py:2:3
  |
1 | src/flext_target_oracle/
2 | ├── settings/
  |   ^
3 | │   ├── environments.py     # Environment-specific configurations
4 | │   ├── schema_evolution.py # Table modification strategies
  |

missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
 --> docs/guides/python-module-organization.md#block8.py:2:13
  |
1 | src/flext_target_oracle/
2 | ├── settings/
  |             ^
3 | │   ├── environments.py     # Environment-specific configurations
4 | │   ├── schema_evolution.py # Table modification strategies
  |
help: Add missing whitespace

invalid-syntax: Expected an expression
 --> docs/guides/python-module-organization.md#block8.py:2:14
  |
1 | src/flext_target_oracle/
2 | ├── settings/
  |              ^
3 | │   ├── environments.py     # Environment-specific configurations
4 | │   ├── schema_evolution.py # Table modification strategies
  |

invalid-syntax: Got unexpected token │
 --> docs/guides/python-module-organization.md#block8.py:3:1
  |
1 | src/flext_target_oracle/
2 | ├── settings/
3 | │   ├── environments.py     # Environment-specific configurations
  | ^
4 | │   ├── schema_evolution.py # Table modification strategies
5 | │   └── performance.py      # Performance optimization settings
  |

invalid-syntax: Got unexpected token ├
 --> docs/guides/python-module-organization.md#block8.py:3:5
  |
1 | src/flext_target_oracle/
2 | ├── settings/
3 | │   ├── environments.py     # Environment-specific configurations
  |     ^
4 | │   ├── schema_evolution.py # Table modification strategies
5 | │   └── performance.py      # Performance optimization settings
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block8.py:3:6
  |
1 | src/flext_target_oracle/
2 | ├── settings/
3 | │   ├── environments.py     # Environment-specific configurations
  |      ^
4 | │   ├── schema_evolution.py # Table modification strategies
5 | │   └── performance.py      # Performance optimization settings
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block8.py:3:7
  |
1 | src/flext_target_oracle/
2 | ├── settings/
3 | │   ├── environments.py     # Environment-specific configurations
  |       ^
4 | │   ├── schema_evolution.py # Table modification strategies
5 | │   └── performance.py      # Performance optimization settings
  |

invalid-syntax: Got unexpected token │
 --> docs/guides/python-module-organization.md#block8.py:4:1
  |
2 | ├── settings/
3 | │   ├── environments.py     # Environment-specific configurations
4 | │   ├── schema_evolution.py # Table modification strategies
  | ^
5 | │   └── performance.py      # Performance optimization settings
6 | ├── observability/
  |

invalid-syntax: Got unexpected token ├
 --> docs/guides/python-module-organization.md#block8.py:4:5
  |
2 | ├── settings/
3 | │   ├── environments.py     # Environment-specific configurations
4 | │   ├── schema_evolution.py # Table modification strategies
  |     ^
5 | │   └── performance.py      # Performance optimization settings
6 | ├── observability/
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block8.py:4:6
  |
2 | ├── settings/
3 | │   ├── environments.py     # Environment-specific configurations
4 | │   ├── schema_evolution.py # Table modification strategies
  |      ^
5 | │   └── performance.py      # Performance optimization settings
6 | ├── observability/
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block8.py:4:7
  |
2 | ├── settings/
3 | │   ├── environments.py     # Environment-specific configurations
4 | │   ├── schema_evolution.py # Table modification strategies
  |       ^
5 | │   └── performance.py      # Performance optimization settings
6 | ├── observability/
  |

too-few-spaces-before-inline-comment: Insert at least two spaces before an inline comment
 --> docs/guides/python-module-organization.md#block8.py:4:28
  |
2 | ├── settings/
3 | │   ├── environments.py     # Environment-specific configurations
4 | │   ├── schema_evolution.py # Table modification strategies
  |                            ^
5 | │   └── performance.py      # Performance optimization settings
6 | ├── observability/
  |
help: Insert spaces

invalid-syntax: Got unexpected token │
 --> docs/guides/python-module-organization.md#block8.py:5:1
  |
3 | │   ├── environments.py     # Environment-specific configurations
4 | │   ├── schema_evolution.py # Table modification strategies
5 | │   └── performance.py      # Performance optimization settings
  | ^
6 | ├── observability/
7 | │   ├── metrics.py          # Custom metrics collection
  |

invalid-syntax: Got unexpected token └
 --> docs/guides/python-module-organization.md#block8.py:5:5
  |
3 | │   ├── environments.py     # Environment-specific configurations
4 | │   ├── schema_evolution.py # Table modification strategies
5 | │   └── performance.py      # Performance optimization settings
  |     ^
6 | ├── observability/
7 | │   ├── metrics.py          # Custom metrics collection
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block8.py:5:6
  |
3 | │   ├── environments.py     # Environment-specific configurations
4 | │   ├── schema_evolution.py # Table modification strategies
5 | │   └── performance.py      # Performance optimization settings
  |      ^
6 | ├── observability/
7 | │   ├── metrics.py          # Custom metrics collection
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block8.py:5:7
  |
3 | │   ├── environments.py     # Environment-specific configurations
4 | │   ├── schema_evolution.py # Table modification strategies
5 | │   └── performance.py      # Performance optimization settings
  |       ^
6 | ├── observability/
7 | │   ├── metrics.py          # Custom metrics collection
  |

invalid-syntax: Got unexpected token ├
 --> docs/guides/python-module-organization.md#block8.py:6:1
  |
4 | │   ├── schema_evolution.py # Table modification strategies
5 | │   └── performance.py      # Performance optimization settings
6 | ├── observability/
  | ^
7 | │   ├── metrics.py          # Custom metrics collection
8 | │   ├── tracing.py          # Distributed tracing integration
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block8.py:6:2
  |
4 | │   ├── schema_evolution.py # Table modification strategies
5 | │   └── performance.py      # Performance optimization settings
6 | ├── observability/
  |  ^
7 | │   ├── metrics.py          # Custom metrics collection
8 | │   ├── tracing.py          # Distributed tracing integration
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block8.py:6:3
  |
4 | │   ├── schema_evolution.py # Table modification strategies
5 | │   └── performance.py      # Performance optimization settings
6 | ├── observability/
  |   ^
7 | │   ├── metrics.py          # Custom metrics collection
8 | │   ├── tracing.py          # Distributed tracing integration
  |

missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
 --> docs/guides/python-module-organization.md#block8.py:6:18
  |
4 | │   ├── schema_evolution.py # Table modification strategies
5 | │   └── performance.py      # Performance optimization settings
6 | ├── observability/
  |                  ^
7 | │   ├── metrics.py          # Custom metrics collection
8 | │   ├── tracing.py          # Distributed tracing integration
  |
help: Add missing whitespace

invalid-syntax: Expected an expression
 --> docs/guides/python-module-organization.md#block8.py:6:19
  |
4 | │   ├── schema_evolution.py # Table modification strategies
5 | │   └── performance.py      # Performance optimization settings
6 | ├── observability/
  |                   ^
7 | │   ├── metrics.py          # Custom metrics collection
8 | │   ├── tracing.py          # Distributed tracing integration
  |

invalid-syntax: Got unexpected token │
 --> docs/guides/python-module-organization.md#block8.py:7:1
  |
5 | │   └── performance.py      # Performance optimization settings
6 | ├── observability/
7 | │   ├── metrics.py          # Custom metrics collection
  | ^
8 | │   ├── tracing.py          # Distributed tracing integration
9 | │   └── health.py           # Health check implementations
  |

invalid-syntax: Got unexpected token ├
 --> docs/guides/python-module-organization.md#block8.py:7:5
  |
5 | │   └── performance.py      # Performance optimization settings
6 | ├── observability/
7 | │   ├── metrics.py          # Custom metrics collection
  |     ^
8 | │   ├── tracing.py          # Distributed tracing integration
9 | │   └── health.py           # Health check implementations
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block8.py:7:6
  |
5 | │   └── performance.py      # Performance optimization settings
6 | ├── observability/
7 | │   ├── metrics.py          # Custom metrics collection
  |      ^
8 | │   ├── tracing.py          # Distributed tracing integration
9 | │   └── health.py           # Health check implementations
  |

invalid-syntax: Got unexpected token ─
 --> docs/guides/python-module-organization.md#block8.py:7:7
  |
5 | │   └── performance.py      # Performance optimization settings
6 | ├── observability/
7 | │   ├── metrics.py          # Custom metrics collection
  |       ^
8 | │   ├── tracing.py          # Distributed tracing integration
9 | │   └── health.py           # Health check implementations
  |

invalid-syntax: Got unexpected token │
  --> docs/guides/python-module-organization.md#block8.py:8:1
   |
 6 | ├── observability/
 7 | │   ├── metrics.py          # Custom metrics collection
 8 | │   ├── tracing.py          # Distributed tracing integration
   | ^
 9 | │   └── health.py           # Health check implementations
10 | └── advanced/
   |

invalid-syntax: Got unexpected token ├
  --> docs/guides/python-module-organization.md#block8.py:8:5
   |
 6 | ├── observability/
 7 | │   ├── metrics.py          # Custom metrics collection
 8 | │   ├── tracing.py          # Distributed tracing integration
   |     ^
 9 | │   └── health.py           # Health check implementations
10 | └── advanced/
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block8.py:8:6
   |
 6 | ├── observability/
 7 | │   ├── metrics.py          # Custom metrics collection
 8 | │   ├── tracing.py          # Distributed tracing integration
   |      ^
 9 | │   └── health.py           # Health check implementations
10 | └── advanced/
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block8.py:8:7
   |
 6 | ├── observability/
 7 | │   ├── metrics.py          # Custom metrics collection
 8 | │   ├── tracing.py          # Distributed tracing integration
   |       ^
 9 | │   └── health.py           # Health check implementations
10 | └── advanced/
   |

invalid-syntax: Got unexpected token │
  --> docs/guides/python-module-organization.md#block8.py:9:1
   |
 7 | │   ├── metrics.py          # Custom metrics collection
 8 | │   ├── tracing.py          # Distributed tracing integration
 9 | │   └── health.py           # Health check implementations
   | ^
10 | └── advanced/
11 |     ├── compression.py      # Oracle compression features
   |

invalid-syntax: Got unexpected token └
  --> docs/guides/python-module-organization.md#block8.py:9:5
   |
 7 | │   ├── metrics.py          # Custom metrics collection
 8 | │   ├── tracing.py          # Distributed tracing integration
 9 | │   └── health.py           # Health check implementations
   |     ^
10 | └── advanced/
11 |     ├── compression.py      # Oracle compression features
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block8.py:9:6
   |
 7 | │   ├── metrics.py          # Custom metrics collection
 8 | │   ├── tracing.py          # Distributed tracing integration
 9 | │   └── health.py           # Health check implementations
   |      ^
10 | └── advanced/
11 |     ├── compression.py      # Oracle compression features
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block8.py:9:7
   |
 7 | │   ├── metrics.py          # Custom metrics collection
 8 | │   ├── tracing.py          # Distributed tracing integration
 9 | │   └── health.py           # Health check implementations
   |       ^
10 | └── advanced/
11 |     ├── compression.py      # Oracle compression features
   |

invalid-syntax: Got unexpected token └
  --> docs/guides/python-module-organization.md#block8.py:10:1
   |
 8 | │   ├── tracing.py          # Distributed tracing integration
 9 | │   └── health.py           # Health check implementations
10 | └── advanced/
   | ^
11 |     ├── compression.py      # Oracle compression features
12 |     ├── partitioning.py     # Table partitioning strategies
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block8.py:10:2
   |
 8 | │   ├── tracing.py          # Distributed tracing integration
 9 | │   └── health.py           # Health check implementations
10 | └── advanced/
   |  ^
11 |     ├── compression.py      # Oracle compression features
12 |     ├── partitioning.py     # Table partitioning strategies
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block8.py:10:3
   |
 8 | │   ├── tracing.py          # Distributed tracing integration
 9 | │   └── health.py           # Health check implementations
10 | └── advanced/
   |   ^
11 |     ├── compression.py      # Oracle compression features
12 |     ├── partitioning.py     # Table partitioning strategies
   |

missing-whitespace-around-arithmetic-operator: Missing whitespace around arithmetic operator
  --> docs/guides/python-module-organization.md#block8.py:10:13
   |
 8 | │   ├── tracing.py          # Distributed tracing integration
 9 | │   └── health.py           # Health check implementations
10 | └── advanced/
   |             ^
11 |     ├── compression.py      # Oracle compression features
12 |     ├── partitioning.py     # Table partitioning strategies
   |
help: Add missing whitespace

invalid-syntax: Expected an expression
  --> docs/guides/python-module-organization.md#block8.py:10:14
   |
 8 | │   ├── tracing.py          # Distributed tracing integration
 9 | │   └── health.py           # Health check implementations
10 | └── advanced/
   |              ^
11 |     ├── compression.py      # Oracle compression features
12 |     ├── partitioning.py     # Table partitioning strategies
   |

invalid-syntax: Unexpected indentation
  --> docs/guides/python-module-organization.md#block8.py:11:1
   |
 9 | │   └── health.py           # Health check implementations
10 | └── advanced/
11 |     ├── compression.py      # Oracle compression features
   | ^^^^
12 |     ├── partitioning.py     # Table partitioning strategies
13 |     └── parallel.py         # Parallel processing optimization
   |

unexpected-indentation: Unexpected indentation
  --> docs/guides/python-module-organization.md#block8.py:11:1
   |
 9 | │   └── health.py           # Health check implementations
10 | └── advanced/
11 |     ├── compression.py      # Oracle compression features
   | ^^^^
12 |     ├── partitioning.py     # Table partitioning strategies
13 |     └── parallel.py         # Parallel processing optimization
   |

invalid-syntax: Got unexpected token ├
  --> docs/guides/python-module-organization.md#block8.py:11:5
   |
 9 | │   └── health.py           # Health check implementations
10 | └── advanced/
11 |     ├── compression.py      # Oracle compression features
   |     ^
12 |     ├── partitioning.py     # Table partitioning strategies
13 |     └── parallel.py         # Parallel processing optimization
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block8.py:11:6
   |
 9 | │   └── health.py           # Health check implementations
10 | └── advanced/
11 |     ├── compression.py      # Oracle compression features
   |      ^
12 |     ├── partitioning.py     # Table partitioning strategies
13 |     └── parallel.py         # Parallel processing optimization
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block8.py:11:7
   |
 9 | │   └── health.py           # Health check implementations
10 | └── advanced/
11 |     ├── compression.py      # Oracle compression features
   |       ^
12 |     ├── partitioning.py     # Table partitioning strategies
13 |     └── parallel.py         # Parallel processing optimization
   |

invalid-syntax: Got unexpected token ├
  --> docs/guides/python-module-organization.md#block8.py:12:5
   |
10 | └── advanced/
11 |     ├── compression.py      # Oracle compression features
12 |     ├── partitioning.py     # Table partitioning strategies
   |     ^
13 |     └── parallel.py         # Parallel processing optimization
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block8.py:12:6
   |
10 | └── advanced/
11 |     ├── compression.py      # Oracle compression features
12 |     ├── partitioning.py     # Table partitioning strategies
   |      ^
13 |     └── parallel.py         # Parallel processing optimization
   |

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block8.py:12:7
   |
10 | └── advanced/
11 |     ├── compression.py      # Oracle compression features
12 |     ├── partitioning.py     # Table partitioning strategies
   |       ^
13 |     └── parallel.py         # Parallel processing optimization
   |

invalid-syntax: Got unexpected token └
  --> docs/guides/python-module-organization.md#block8.py:13:5
   |
11 |     ├── compression.py      # Oracle compression features
12 |     ├── partitioning.py     # Table partitioning strategies
13 |     └── parallel.py         # Parallel processing optimization
   |     ^

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block8.py:13:6
   |
11 |     ├── compression.py      # Oracle compression features
12 |     ├── partitioning.py     # Table partitioning strategies
13 |     └── parallel.py         # Parallel processing optimization
   |      ^

invalid-syntax: Got unexpected token ─
  --> docs/guides/python-module-organization.md#block8.py:13:7
   |
11 |     ├── compression.py      # Oracle compression features
12 |     ├── partitioning.py     # Table partitioning strategies
13 |     └── parallel.py         # Parallel processing optimization
   |       ^

Found 54 errors. |
| docs/guides/singer-integration.md | python_codeblock | medium | block #0: blank-lines-top-level: Expected 2 blank lines, found 0
  --> docs/guides/singer-integration.md#block0.py:11:1
   |
 9 |     Sequence,
10 | )
11 | def _handle_state(self, message: p.Dict) -> p.Result[bool]:
   | ^^^
12 |     """Handle STATE message - forwarded to orchestrator."""
13 |     # State messages are typically handled by Meltano/orchestrator
   |
help: Add missing blank line(s)

invalid-syntax: Expected an identifier
  --> docs/guides/singer-integration.md#block0.py:15:20
   |
13 |     # State messages are typically handled by Meltano/orchestrator
14 |     logger.debug("State message received - forwarding to Meltano")
15 |     return r[bool].| ok(value=True)
   |                    ^

missing-whitespace-around-bitwise-or-shift-operator: Missing whitespace around bitwise or shift operator
  --> docs/guides/singer-integration.md#block0.py:15:20
   |
13 |     # State messages are typically handled by Meltano/orchestrator
14 |     logger.debug("State message received - forwarding to Meltano")
15 |     return r[bool].| ok(value=True)
   |                    ^
help: Add missing whitespace

Found 3 errors. |
| docs/guides/singer-integration.md | python_codeblock | medium | block #1: blank-lines-top-level: Expected 2 blank lines, found 0
  --> docs/guides/singer-integration.md#block1.py:12:1
   |
10 | )
11 | # ❌ Custom method - not Singer SDK compliant
12 | def process_singer_message(self, message: dict) -> p.Result[bool]:
   | ^^^
13 |     # Custom message processing
   |
help: Add missing blank line(s)

invalid-syntax: Expected an indented block after function definition
  --> docs/guides/singer-integration.md#block1.py:12:67
   |
10 | )
11 | # ❌ Custom method - not Singer SDK compliant
12 | def process_singer_message(self, message: dict) -> p.Result[bool]:
   |                                                                   ^
13 |     # Custom message processing
   |

Found 2 errors. |
| docs/guides/singer-integration.md | python_codeblock | medium | block #2: blank-lines-top-level: Expected 2 blank lines, found 0
  --> docs/guides/singer-integration.md#block2.py:12:1
   |
10 | )
11 | # Current implementation (needs improvement)
12 | def _insert_batch(self, table_name: str, records: list) -> p.Result[bool]:
   | ^^^
13 |     """Insert batch with basic error handling."""
14 |     try:
   |
help: Add missing blank line(s)

invalid-syntax: Expected an identifier
  --> docs/guides/singer-integration.md#block2.py:22:24
   |
20 |                     return r[bool].fail(f"Insert failed: {result.error}")
21 |
22 |         return r[bool].| ok(value=True)
   |                        ^
23 |
24 |     except Exception as e:
   |

missing-whitespace-around-bitwise-or-shift-operator: Missing whitespace around bitwise or shift operator
  --> docs/guides/singer-integration.md#block2.py:22:24
   |
20 |                     return r[bool].fail(f"Insert failed: {result.error}")
21 |
22 |         return r[bool].| ok(value=True)
   |                        ^
23 |
24 |     except Exception as e:
   |
help: Add missing whitespace

blank-lines-top-level: Expected 2 blank lines, found 1
  --> docs/guides/singer-integration.md#block2.py:28:1
   |
27 | # Improved implementation (needed)
28 | def _insert_batch_improved(self, table_name: str, records: list) -> p.Result[bool]:
   | ^^^
29 |     """Insert batch with proper transaction management."""
30 |     try:
   |
help: Add missing blank line(s)

invalid-syntax: Expected an identifier
  --> docs/guides/singer-integration.md#block2.py:42:24
   |
40 |                 connected_api.commit()
41 |
42 |         return r[bool].| ok(value=True)
   |                        ^
43 |
44 |     except Exception as e:
   |

missing-whitespace-around-bitwise-or-shift-operator: Missing whitespace around bitwise or shift operator
  --> docs/guides/singer-integration.md#block2.py:42:24
   |
40 |                 connected_api.commit()
41 |
42 |         return r[bool].| ok(value=True)
   |                        ^
43 |
44 |     except Exception as e:
   |
help: Add missing whitespace

Found 6 errors. |
| docs/security/snyk-sast-triage.md | python_codeblock | medium | block #0: indentation-with-invalid-multiple: Indentation is not a multiple of 4
 --> docs/security/snyk-sast-triage.md#block0.py:1:1
  |
1 |        85              "host": os.environ["TEST_ORACLE_HOST"],
  | ^^^^^^^
2 |        86              "port": int(os.environ["TEST_ORACLE_PORT"]),
3 |        87              c.ContextKey.SERVICE_NAME: os.environ["TEST_ORACLE_SERVICE"],
  |

invalid-syntax: Unexpected indentation
 --> docs/security/snyk-sast-triage.md#block0.py:1:1
  |
1 |        85              "host": os.environ["TEST_ORACLE_HOST"],
  | ^^^^^^^
2 |        86              "port": int(os.environ["TEST_ORACLE_PORT"]),
3 |        87              c.ContextKey.SERVICE_NAME: os.environ["TEST_ORACLE_SERVICE"],
  |

invalid-syntax: Simple statements must be separated by newlines or semicolons
 --> docs/security/snyk-sast-triage.md#block0.py:1:24
  |
1 |        85              "host": os.environ["TEST_ORACLE_HOST"],
  |                        ^^^^^^
2 |        86              "port": int(os.environ["TEST_ORACLE_PORT"]),
3 |        87              c.ContextKey.SERVICE_NAME: os.environ["TEST_ORACLE_SERVICE"],
  |

invalid-syntax: Expected a statement
 --> docs/security/snyk-sast-triage.md#block0.py:1:62
  |
1 |        85              "host": os.environ["TEST_ORACLE_HOST"],
  |                                                              ^
2 |        86              "port": int(os.environ["TEST_ORACLE_PORT"]),
3 |        87              c.ContextKey.SERVICE_NAME: os.environ["TEST_ORACLE_SERVICE"],
  |

trailing-comma-on-bare-tuple: Trailing comma on bare tuple prohibited
 --> docs/security/snyk-sast-triage.md#block0.py:1:62
  |
1 |        85              "host": os.environ["TEST_ORACLE_HOST"],
  |                                                              ^
2 |        86              "port": int(os.environ["TEST_ORACLE_PORT"]),
3 |        87              c.ContextKey.SERVICE_NAME: os.environ["TEST_ORACLE_SERVICE"],
  |

invalid-syntax: Expected a statement
 --> docs/security/snyk-sast-triage.md#block0.py:1:63
  |
1 |        85              "host": os.environ["TEST_ORACLE_HOST"],
  |                                                               ^
2 |        86              "port": int(os.environ["TEST_ORACLE_PORT"]),
3 |        87              c.ContextKey.SERVICE_NAME: os.environ["TEST_ORACLE_SERVICE"],
  |

indentation-with-invalid-multiple: Indentation is not a multiple of 4
 --> docs/security/snyk-sast-triage.md#block0.py:2:1
  |
1 |        85              "host": os.environ["TEST_ORACLE_HOST"],
2 |        86              "port": int(os.environ["TEST_ORACLE_PORT"]),
  | ^^^^^^^
3 |        87              c.ContextKey.SERVICE_NAME: os.environ["TEST_ORACLE_SERVICE"],
4 |        88              "username": "system",
  |

invalid-syntax: Simple statements must be separated by newlines or semicolons
 --> docs/security/snyk-sast-triage.md#block0.py:2:24
  |
1 |        85              "host": os.environ["TEST_ORACLE_HOST"],
2 |        86              "port": int(os.environ["TEST_ORACLE_PORT"]),
  |                        ^^^^^^
3 |        87              c.ContextKey.SERVICE_NAME: os.environ["TEST_ORACLE_SERVICE"],
4 |        88              "username": "system",
  |

invalid-syntax: Expected a statement
 --> docs/security/snyk-sast-triage.md#block0.py:2:67
  |
1 |        85              "host": os.environ["TEST_ORACLE_HOST"],
2 |        86              "port": int(os.environ["TEST_ORACLE_PORT"]),
  |                                                                   ^
3 |        87              c.ContextKey.SERVICE_NAME: os.environ["TEST_ORACLE_SERVICE"],
4 |        88              "username": "system",
  |

trailing-comma-on-bare-tuple: Trailing comma on bare tuple prohibited
 --> docs/security/snyk-sast-triage.md#block0.py:2:67
  |
1 |        85              "host": os.environ["TEST_ORACLE_HOST"],
2 |        86              "port": int(os.environ["TEST_ORACLE_PORT"]),
  |                                                                   ^
3 |        87              c.ContextKey.SERVICE_NAME: os.environ["TEST_ORACLE_SERVICE"],
4 |        88              "username": "system",
  |

invalid-syntax: Expected a statement
 --> docs/security/snyk-sast-triage.md#block0.py:2:68
  |
1 |        85              "host": os.environ["TEST_ORACLE_HOST"],
2 |        86              "port": int(os.environ["TEST_ORACLE_PORT"]),
  |                                                                    ^
3 |        87              c.ContextKey.SERVICE_NAME: os.environ["TEST_ORACLE_SERVICE"],
4 |        88              "username": "system",
  |

indentation-with-invalid-multiple: Indentation is not a multiple of 4
 --> docs/security/snyk-sast-triage.md#block0.py:3:1
  |
1 |        85              "host": os.environ["TEST_ORACLE_HOST"],
2 |        86              "port": int(os.environ["TEST_ORACLE_PORT"]),
3 |        87              c.ContextKey.SERVICE_NAME: os.environ["TEST_ORACLE_SERVICE"],
  | ^^^^^^^
4 |        88              "username": "system",
5 | >>>    89              "password": "flext_oracle_test",
  |

invalid-syntax: Simple statements must be separated by newlines or semicolons
 --> docs/security/snyk-sast-triage.md#block0.py:3:24
  |
1 |        85              "host": os.environ["TEST_ORACLE_HOST"],
2 |        86              "port": int(os.environ["TEST_ORACLE_PORT"]),
3 |        87              c.ContextKey.SERVICE_NAME: os.environ["TEST_ORACLE_SERVICE"],
  |                        ^
4 |        88              "username": "system",
5 | >>>    89              "password": "flext_oracle_test",
  |

invalid-syntax: Expected a statement
 --> docs/security/snyk-sast-triage.md#block0.py:3:84
  |
1 |        85              "host": os.environ["TEST_ORACLE_HOST"],
2 |        86              "port": int(os.environ["TEST_ORACLE_PORT"]),
3 |        87              c.ContextKey.SERVICE_NAME: os.environ["TEST_ORACLE_SERVICE"],
  |                                                                                    ^
4 |        88              "username": "system",
5 | >>>    89              "password": "flext_oracle_test",
  |

trailing-comma-on-bare-tuple: Trailing comma on bare tuple prohibited
 --> docs/security/snyk-sast-triage.md#block0.py:3:84
  |
1 |        85              "host": os.environ["TEST_ORACLE_HOST"],
2 |        86              "port": int(os.environ["TEST_ORACLE_PORT"]),
3 |        87              c.ContextKey.SERVICE_NAME: os.environ["TEST_ORACLE_SERVICE"],
  |                                                                                    ^
4 |        88              "username": "system",
5 | >>>    89              "password": "flext_oracle_test",
  |

invalid-syntax: Expected a statement
 --> docs/security/snyk-sast-triage.md#block0.py:3:85
  |
1 |        85              "host": os.environ["TEST_ORACLE_HOST"],
2 |        86              "port": int(os.environ["TEST_ORACLE_PORT"]),
3 |        87              c.ContextKey.SERVICE_NAME: os.environ["TEST_ORACLE_SERVICE"],
  |                                                                                     ^
4 |        88              "username": "system",
5 | >>>    89              "password": "flext_oracle_test",
  |

indentation-with-invalid-multiple: Indentation is not a multiple of 4
 --> docs/security/snyk-sast-triage.md#block0.py:4:1
  |
2 |        86              "port": int(os.environ["TEST_ORACLE_PORT"]),
3 |        87              c.ContextKey.SERVICE_NAME: os.environ["TEST_ORACLE_SERVICE"],
4 |        88              "username": "system",
  | ^^^^^^^
5 | >>>    89              "password": "flext_oracle_test",
6 |        90          }
  |

invalid-syntax: Simple statements must be separated by newlines or semicolons
 --> docs/security/snyk-sast-triage.md#block0.py:4:24
  |
2 |        86              "port": int(os.environ["TEST_ORACLE_PORT"]),
3 |        87              c.ContextKey.SERVICE_NAME: os.environ["TEST_ORACLE_SERVICE"],
4 |        88              "username": "system",
  |                        ^^^^^^^^^^
5 | >>>    89              "password": "flext_oracle_test",
6 |        90          }
  |

trailing-comma-on-bare-tuple: Trailing comma on bare tuple prohibited
 --> docs/security/snyk-sast-triage.md#block0.py:4:44
  |
2 |        86              "port": int(os.environ["TEST_ORACLE_PORT"]),
3 |        87              c.ContextKey.SERVICE_NAME: os.environ["TEST_ORACLE_SERVICE"],
4 |        88              "username": "system",
  |                                            ^
5 | >>>    89              "password": "flext_oracle_test",
6 |        90          }
  |

invalid-syntax: Expected a statement
 --> docs/security/snyk-sast-triage.md#block0.py:4:44
  |
2 |        86              "port": int(os.environ["TEST_ORACLE_PORT"]),
3 |        87              c.ContextKey.SERVICE_NAME: os.environ["TEST_ORACLE_SERVICE"],
4 |        88              "username": "system",
  |                                            ^
5 | >>>    89              "password": "flext_oracle_test",
6 |        90          }
  |

invalid-syntax: Expected a statement
 --> docs/security/snyk-sast-triage.md#block0.py:4:45
  |
2 |        86              "port": int(os.environ["TEST_ORACLE_PORT"]),
3 |        87              c.ContextKey.SERVICE_NAME: os.environ["TEST_ORACLE_SERVICE"],
4 |        88              "username": "system",
  |                                             ^
5 | >>>    89              "password": "flext_oracle_test",
6 |        90          }
  |

invalid-syntax: Expected a statement
 --> docs/security/snyk-sast-triage.md#block0.py:5:1
  |
3 |        87              c.ContextKey.SERVICE_NAME: os.environ["TEST_ORACLE_SERVICE"],
4 |        88              "username": "system",
5 | >>>    89              "password": "flext_oracle_test",
  | ^^
6 |        90          }
7 |        91      })
  |

invalid-syntax: Expected a statement
 --> docs/security/snyk-sast-triage.md#block0.py:5:3
  |
3 |        87              c.ContextKey.SERVICE_NAME: os.environ["TEST_ORACLE_SERVICE"],
4 |        88              "username": "system",
5 | >>>    89              "password": "flext_oracle_test",
  |   ^
6 |        90          }
7 |        91      })
  |

missing-whitespace-around-operator: Missing whitespace around operator
 --> docs/security/snyk-sast-triage.md#block0.py:5:3
  |
3 |        87              c.ContextKey.SERVICE_NAME: os.environ["TEST_ORACLE_SERVICE"],
4 |        88              "username": "system",
5 | >>>    89              "password": "flext_oracle_test",
  |   ^
6 |        90          }
7 |        91      })
  |
help: Add missing whitespace

multiple-spaces-after-operator: Multiple spaces after operator
 --> docs/security/snyk-sast-triage.md#block0.py:5:4
  |
3 |        87              c.ContextKey.SERVICE_NAME: os.environ["TEST_ORACLE_SERVICE"],
4 |        88              "username": "system",
5 | >>>    89              "password": "flext_oracle_test",
  |    ^^^^
6 |        90          }
7 |        91      })
  |
help: Replace with single space

invalid-syntax: Simple statements must be separated by newlines or semicolons
 --> docs/security/snyk-sast-triage.md#block0.py:5:24
  |
3 |        87              c.ContextKey.SERVICE_NAME: os.environ["TEST_ORACLE_SERVICE"],
4 |        88              "username": "system",
5 | >>>    89              "password": "flext_oracle_test",
  |                        ^^^^^^^^^^
6 |        90          }
7 |        91      })
  |

invalid-syntax: Expected a statement
 --> docs/security/snyk-sast-triage.md#block0.py:5:55
  |
3 |        87              c.ContextKey.SERVICE_NAME: os.environ["TEST_ORACLE_SERVICE"],
4 |        88              "username": "system",
5 | >>>    89              "password": "flext_oracle_test",
  |                                                       ^
6 |        90          }
7 |        91      })
  |

trailing-comma-on-bare-tuple: Trailing comma on bare tuple prohibited
 --> docs/security/snyk-sast-triage.md#block0.py:5:55
  |
3 |        87              c.ContextKey.SERVICE_NAME: os.environ["TEST_ORACLE_SERVICE"],
4 |        88              "username": "system",
5 | >>>    89              "password": "flext_oracle_test",
  |                                                       ^
6 |        90          }
7 |        91      })
  |

invalid-syntax: Expected a statement
 --> docs/security/snyk-sast-triage.md#block0.py:5:56
  |
3 |        87              c.ContextKey.SERVICE_NAME: os.environ["TEST_ORACLE_SERVICE"],
4 |        88              "username": "system",
5 | >>>    89              "password": "flext_oracle_test",
  |                                                        ^
6 |        90          }
7 |        91      })
  |

invalid-syntax: Unexpected indentation
 --> docs/security/snyk-sast-triage.md#block0.py:6:1
  |
4 |        88              "username": "system",
5 | >>>    89              "password": "flext_oracle_test",
6 |        90          }
  | ^^^^^^^
7 |        91      })
8 |        92      oracle_settings = FlextDbOracleSettings.model_validate({
  |

indentation-with-invalid-multiple: Indentation is not a multiple of 4
 --> docs/security/snyk-sast-triage.md#block0.py:6:1
  |
4 |        88              "username": "system",
5 | >>>    89              "password": "flext_oracle_test",
6 |        90          }
  | ^^^^^^^
7 |        91      })
8 |        92      oracle_settings = FlextDbOracleSettings.model_validate({
  |

unexpected-indentation: Unexpected indentation
 --> docs/security/snyk-sast-triage.md#block0.py:6:1
  |
4 |        88              "username": "system",
5 | >>>    89              "password": "flext_oracle_test",
6 |        90          }
  | ^^^^^^^
7 |        91      })
8 |        92      oracle_settings = FlextDbOracleSettings.model_validate({
  |

whitespace-before-close-bracket: Whitespace before '}'
 --> docs/security/snyk-sast-triage.md#block0.py:6:10
  |
4 |        88              "username": "system",
5 | >>>    89              "password": "flext_oracle_test",
6 |        90          }
  |          ^^^^^^^^^^
7 |        91      })
8 |        92      oracle_settings = FlextDbOracleSettings.model_validate({
  |
help: Remove whitespace before '}'

invalid-syntax: Expected a statement
 --> docs/security/snyk-sast-triage.md#block0.py:6:20
  |
4 |        88              "username": "system",
5 | >>>    89              "password": "flext_oracle_test",
6 |        90          }
  |                    ^
7 |        91      })
8 |        92      oracle_settings = FlextDbOracleSettings.model_validate({
  |

invalid-syntax: Expected a statement
 --> docs/security/snyk-sast-triage.md#block0.py:6:21
  |
4 |        88              "username": "system",
5 | >>>    89              "password": "flext_oracle_test",
6 |        90          }
  |                     ^
7 |        91      })
8 |        92      oracle_settings = FlextDbOracleSettings.model_validate({
  |

indentation-with-invalid-multiple: Indentation is not a multiple of 4
 --> docs/security/snyk-sast-triage.md#block0.py:7:1
  |
5 | >>>    89              "password": "flext_oracle_test",
6 |        90          }
7 |        91      })
  | ^^^^^^^
8 |        92      oracle_settings = FlextDbOracleSettings.model_validate({
9 |        93          "DbOracle": {
  |

whitespace-before-close-bracket: Whitespace before '}'
 --> docs/security/snyk-sast-triage.md#block0.py:7:10
  |
5 | >>>    89              "password": "flext_oracle_test",
6 |        90          }
7 |        91      })
  |          ^^^^^^
8 |        92      oracle_settings = FlextDbOracleSettings.model_validate({
9 |        93          "DbOracle": {
  |
help: Remove whitespace before '}'

invalid-syntax: Expected a statement
 --> docs/security/snyk-sast-triage.md#block0.py:7:16
  |
5 | >>>    89              "password": "flext_oracle_test",
6 |        90          }
7 |        91      })
  |                ^
8 |        92      oracle_settings = FlextDbOracleSettings.model_validate({
9 |        93          "DbOracle": {
  |

invalid-syntax: Expected a statement
 --> docs/security/snyk-sast-triage.md#block0.py:7:17
  |
5 | >>>    89              "password": "flext_oracle_test",
6 |        90          }
7 |        91      })
  |                 ^
8 |        92      oracle_settings = FlextDbOracleSettings.model_validate({
9 |        93          "DbOracle": {
  |

invalid-syntax: Expected a statement
 --> docs/security/snyk-sast-triage.md#block0.py:7:18
  |
5 | >>>    89              "password": "flext_oracle_test",
6 |        90          }
7 |        91      })
  |                  ^
8 |        92      oracle_settings = FlextDbOracleSettings.model_validate({
9 |        93          "DbOracle": {
  |

indentation-with-invalid-multiple: Indentation is not a multiple of 4
 --> docs/security/snyk-sast-triage.md#block0.py:8:1
  |
6 |        90          }
7 |        91      })
8 |        92      oracle_settings = FlextDbOracleSettings.model_validate({
  | ^^^^^^^
9 |        93          "DbOracle": {
  |

invalid-syntax: Simple statements must be separated by newlines or semicolons
 --> docs/security/snyk-sast-triage.md#block0.py:8:16
  |
6 |        90          }
7 |        91      })
8 |        92      oracle_settings = FlextDbOracleSettings.model_validate({
  |                ^^^^^^^^^^^^^^^
9 |        93          "DbOracle": {
  |

invalid-syntax: Expected `,`, found string
 --> docs/security/snyk-sast-triage.md#block0.py:9:20
  |
7 |        91      })
8 |        92      oracle_settings = FlextDbOracleSettings.model_validate({
9 |        93          "DbOracle": {
  |                    ^^^^^^^^^^

invalid-syntax: Expected `,`, found `:`
 --> docs/security/snyk-sast-triage.md#block0.py:9:30
  |
7 |        91      })
8 |        92      oracle_settings = FlextDbOracleSettings.model_validate({
9 |        93          "DbOracle": {
  |                              ^

invalid-syntax: unexpected EOF while parsing
 --> docs/security/snyk-sast-triage.md#block0.py:9:34
  |
8 |        92      oracle_settings = FlextDbOracleSettings.model_validate({
9 |        93          "DbOracle": {
  |                                 ^

Found 45 errors. |
| docs/security/snyk-sast-triage.md | python_codeblock | medium | block #1: invalid-syntax: Unexpected indentation
 --> docs/security/snyk-sast-triage.md#block1.py:1:1
  |
1 |       472              "record": {
  | ^^^^^^
2 |       473                  "id": 1,
3 |       474                  "name": "John Doe",
  |

indentation-with-invalid-multiple: Indentation is not a multiple of 4
 --> docs/security/snyk-sast-triage.md#block1.py:1:1
  |
1 |       472              "record": {
  | ^^^^^^
2 |       473                  "id": 1,
3 |       474                  "name": "John Doe",
  |

invalid-syntax: Simple statements must be separated by newlines or semicolons
 --> docs/security/snyk-sast-triage.md#block1.py:1:24
  |
1 |       472              "record": {
  |                        ^^^^^^^^
2 |       473                  "id": 1,
3 |       474                  "name": "John Doe",
  |

invalid-syntax: Expected `,`, found string
 --> docs/security/snyk-sast-triage.md#block1.py:2:28
  |
1 |       472              "record": {
2 |       473                  "id": 1,
  |                            ^^^^
3 |       474                  "name": "John Doe",
4 |       475                  "email": "john@example.com",
  |

invalid-syntax: Expected `,`, found `:`
 --> docs/security/snyk-sast-triage.md#block1.py:2:32
  |
1 |       472              "record": {
2 |       473                  "id": 1,
  |                                ^
3 |       474                  "name": "John Doe",
4 |       475                  "email": "john@example.com",
  |

invalid-syntax: Expected `,`, found string
 --> docs/security/snyk-sast-triage.md#block1.py:3:28
  |
1 |       472              "record": {
2 |       473                  "id": 1,
3 |       474                  "name": "John Doe",
  |                            ^^^^^^
4 |       475                  "email": "john@example.com",
5 | >>>   476                  "password": "secret123",
  |

invalid-syntax: Expected `,`, found `:`
 --> docs/security/snyk-sast-triage.md#block1.py:3:34
  |
1 |       472              "record": {
2 |       473                  "id": 1,
3 |       474                  "name": "John Doe",
  |                                  ^
4 |       475                  "email": "john@example.com",
5 | >>>   476                  "password": "secret123",
  |

invalid-syntax: Expected `,`, found string
 --> docs/security/snyk-sast-triage.md#block1.py:4:28
  |
2 |       473                  "id": 1,
3 |       474                  "name": "John Doe",
4 |       475                  "email": "john@example.com",
  |                            ^^^^^^^
5 | >>>   476                  "password": "secret123",
6 |       477                  "internal_id": "INT-001",
  |

invalid-syntax: Expected `,`, found `:`
 --> docs/security/snyk-sast-triage.md#block1.py:4:35
  |
2 |       473                  "id": 1,
3 |       474                  "name": "John Doe",
4 |       475                  "email": "john@example.com",
  |                                   ^
5 | >>>   476                  "password": "secret123",
6 |       477                  "internal_id": "INT-001",
  |

invalid-syntax: Expected `,`, found `>>`
 --> docs/security/snyk-sast-triage.md#block1.py:5:1
  |
3 |       474                  "name": "John Doe",
4 |       475                  "email": "john@example.com",
5 | >>>   476                  "password": "secret123",
  | ^^
6 |       477                  "internal_id": "INT-001",
7 |       478              },
  |

missing-whitespace-around-bitwise-or-shift-operator: Missing whitespace around bitwise or shift operator
 --> docs/security/snyk-sast-triage.md#block1.py:5:1
  |
3 |       474                  "name": "John Doe",
4 |       475                  "email": "john@example.com",
5 | >>>   476                  "password": "secret123",
  | ^^
6 |       477                  "internal_id": "INT-001",
7 |       478              },
  |
help: Add missing whitespace

invalid-syntax: Expected `,`, found `>`
 --> docs/security/snyk-sast-triage.md#block1.py:5:3
  |
3 |       474                  "name": "John Doe",
4 |       475                  "email": "john@example.com",
5 | >>>   476                  "password": "secret123",
  |   ^
6 |       477                  "internal_id": "INT-001",
7 |       478              },
  |

missing-whitespace-around-operator: Missing whitespace around operator
 --> docs/security/snyk-sast-triage.md#block1.py:5:3
  |
3 |       474                  "name": "John Doe",
4 |       475                  "email": "john@example.com",
5 | >>>   476                  "password": "secret123",
  |   ^
6 |       477                  "internal_id": "INT-001",
7 |       478              },
  |
help: Add missing whitespace

multiple-spaces-after-operator: Multiple spaces after operator
 --> docs/security/snyk-sast-triage.md#block1.py:5:4
  |
3 |       474                  "name": "John Doe",
4 |       475                  "email": "john@example.com",
5 | >>>   476                  "password": "secret123",
  |    ^^^
6 |       477                  "internal_id": "INT-001",
7 |       478              },
  |
help: Replace with single space

invalid-syntax: Expected `,`, found string
 --> docs/security/snyk-sast-triage.md#block1.py:5:28
  |
3 |       474                  "name": "John Doe",
4 |       475                  "email": "john@example.com",
5 | >>>   476                  "password": "secret123",
  |                            ^^^^^^^^^^
6 |       477                  "internal_id": "INT-001",
7 |       478              },
  |

invalid-syntax: Expected `,`, found `:`
 --> docs/security/snyk-sast-triage.md#block1.py:5:38
  |
3 |       474                  "name": "John Doe",
4 |       475                  "email": "john@example.com",
5 | >>>   476                  "password": "secret123",
  |                                      ^
6 |       477                  "internal_id": "INT-001",
7 |       478              },
  |

invalid-syntax: Expected `,`, found string
 --> docs/security/snyk-sast-triage.md#block1.py:6:28
  |
4 |       475                  "email": "john@example.com",
5 | >>>   476                  "password": "secret123",
6 |       477                  "internal_id": "INT-001",
  |                            ^^^^^^^^^^^^^
7 |       478              },
8 |       479          }
  |

invalid-syntax: Expected `,`, found `:`
 --> docs/security/snyk-sast-triage.md#block1.py:6:41
  |
4 |       475                  "email": "john@example.com",
5 | >>>   476                  "password": "secret123",
6 |       477                  "internal_id": "INT-001",
  |                                         ^
7 |       478              },
8 |       479          }
  |

whitespace-before-close-bracket: Whitespace before '}'
 --> docs/security/snyk-sast-triage.md#block1.py:7:10
  |
5 | >>>   476                  "password": "secret123",
6 |       477                  "internal_id": "INT-001",
7 |       478              },
  |          ^^^^^^^^^^^^^^
8 |       479          }
9 |       480          record_msg_value: t.JsonValue = t.json_value_adapter().validate_python(
  |
help: Remove whitespace before '}'

invalid-syntax: Expected a statement
 --> docs/security/snyk-sast-triage.md#block1.py:7:25
  |
5 | >>>   476                  "password": "secret123",
6 |       477                  "internal_id": "INT-001",
7 |       478              },
  |                         ^
8 |       479          }
9 |       480          record_msg_value: t.JsonValue = t.json_value_adapter().validate_python(
  |

trailing-comma-on-bare-tuple: Trailing comma on bare tuple prohibited
 --> docs/security/snyk-sast-triage.md#block1.py:7:25
  |
5 | >>>   476                  "password": "secret123",
6 |       477                  "internal_id": "INT-001",
7 |       478              },
  |                         ^
8 |       479          }
9 |       480          record_msg_value: t.JsonValue = t.json_value_adapter().validate_python(
  |

invalid-syntax: Expected a statement
 --> docs/security/snyk-sast-triage.md#block1.py:7:26
  |
5 | >>>   476                  "password": "secret123",
6 |       477                  "internal_id": "INT-001",
7 |       478              },
  |                          ^
8 |       479          }
9 |       480          record_msg_value: t.JsonValue = t.json_value_adapter().validate_python(
  |

indentation-with-invalid-multiple: Indentation is not a multiple of 4
 --> docs/security/snyk-sast-triage.md#block1.py:8:1
  |
6 |       477                  "internal_id": "INT-001",
7 |       478              },
8 |       479          }
  | ^^^^^^
9 |       480          record_msg_value: t.JsonValue = t.json_value_adapter().validate_python(
  |

whitespace-before-close-bracket: Whitespace before '}'
 --> docs/security/snyk-sast-triage.md#block1.py:8:10
  |
6 |       477                  "internal_id": "INT-001",
7 |       478              },
8 |       479          }
  |          ^^^^^^^^^^
9 |       480          record_msg_value: t.JsonValue = t.json_value_adapter().validate_python(
  |
help: Remove whitespace before '}'

invalid-syntax: Expected a statement
 --> docs/security/snyk-sast-triage.md#block1.py:8:20
  |
6 |       477                  "internal_id": "INT-001",
7 |       478              },
8 |       479          }
  |                    ^
9 |       480          record_msg_value: t.JsonValue = t.json_value_adapter().validate_python(
  |

invalid-syntax: Expected a statement
 --> docs/security/snyk-sast-triage.md#block1.py:8:21
  |
6 |       477                  "internal_id": "INT-001",
7 |       478              },
8 |       479          }
  |                     ^
9 |       480          record_msg_value: t.JsonValue = t.json_value_adapter().validate_python(
  |

indentation-with-invalid-multiple: Indentation is not a multiple of 4
 --> docs/security/snyk-sast-triage.md#block1.py:9:1
  |
7 |       478              },
8 |       479          }
9 |       480          record_msg_value: t.JsonValue = t.json_value_adapter().validate_python(
  | ^^^^^^

invalid-syntax: Simple statements must be separated by newlines or semicolons
 --> docs/security/snyk-sast-triage.md#block1.py:9:20
  |
7 |       478              },
8 |       479          }
9 |       480          record_msg_value: t.JsonValue = t.json_value_adapter().validate_python(
  |                    ^^^^^^^^^^^^^^^^

line-too-long: Line too long (90 > 88)
 --> docs/security/snyk-sast-triage.md#block1.py:9:89
  |
7 |       478              },
8 |       479          }
9 |       480          record_msg_value: t.JsonValue = t.json_value_adapter().validate_python(
  |                                                                                         ^^

invalid-syntax: unexpected EOF while parsing
 --> docs/security/snyk-sast-triage.md#block1.py:9:92
  |
8 |       479          }
9 |       480          record_msg_value: t.JsonValue = t.json_value_adapter().validate_python(
  |                                                                                           ^

Found 30 errors. |
