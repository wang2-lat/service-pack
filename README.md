# Service Pack

Standardize freelance services and generate quotes instantly.

## Problem

Freelancers struggle to balance client work with building their own products. Without standardized services, they waste time negotiating prices and processes with each client.

## Solution

Service Pack helps you:
- Create standardized service packages with fixed prices and deliverables
- Generate professional quotes instantly
- Track projects and revenue

## Installation


## Usage

### Service Management

Create a service package:

List all services:

Delete a service:

### Quote Generation

Generate a quote:

List all quotes:

### Project Tracking

Add a project from a quote:

List all projects:

Update project status:

View statistics:

## Data Storage

All data is stored in `~/.service-pack/` as JSON files:
- `services.json` - Service packages
- `quotes.json` - Generated quotes
- `projects.json` - Project tracking

## Example Workflow

1. Create service packages for your common offerings
2. When a client inquires, generate a quote by selecting a service
3. Once accepted, add the quote as a project
4. Update project status as you work
5. View stats to track your revenue and time allocation
pip install -r requirements.txt
python main.py service create  # 创建第一个服务包
python main.py quote generate  # 生成报价
python main.py project stats   # 查看收入统计