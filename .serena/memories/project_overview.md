# FLEXT Target Oracle - Project Overview

## Purpose
Production-grade Singer target for Oracle Database data loading, built with FLEXT ecosystem patterns and reliability standards. This is a core component of the FLEXT data integration platform that implements the Singer specification for standardized data integration workflows.

## Tech Stack
- **Language**: Python 3.13+
- **Framework**: FLEXT ecosystem (flext-core, flext-meltano, flext-db-oracle)
- **Database**: Oracle Database 11g+ (tested through 23c)
- **Protocol**: Singer SDK for data integration
- **Architecture**: Clean Architecture + Domain-Driven Design (DDD)
- **Quality**: Zero-tolerance quality gates with 90%+ test coverage requirement

## Key Capabilities
- Enterprise Oracle Integration with advanced features
- Singer Protocol Compliance with full SDK implementation
- FLEXT Pattern Integration using flext-core foundations
- High-Performance Loading with optimized batch processing
- Production-Ready Architecture with Clean Architecture + DDD
- Zero-Tolerance Quality with strict quality enforcement

## Current Status
- **Version**: 0.9.0
- **Documentation**: 95% complete with enterprise-grade standards
- **Implementation**: Critical security vulnerabilities block production deployment
- **Priority**: Fix SQL injection vulnerability and implement missing Singer SDK methods

## Dependencies
- flext-core: Foundational patterns (FlextResult, FlextModels.Value, logging)
- flext-meltano: Singer SDK integration and Target base classes
- flext-db-oracle: Oracle database operations and connectivity
- flext-cli: CLI framework for command-line interfaces
- Singer SDK: Data integration protocol implementation