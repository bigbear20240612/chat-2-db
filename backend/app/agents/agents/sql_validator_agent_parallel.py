"""
SQL验证代理 - 并行处理版本
基于LangGraph并行工作流模式，将语法、安全性、性能验证并行执行
参考: https://langchain-ai.github.io/langgraph/tutorials/workflows/#parallelization
"""
import re
import sqlparse
from typing import Dict, Any, List, Annotated
import operator
# type: ignore  MC80OmFIVnBZMlhucUx2b2pZbmt1cm82UW5CT053PT06ZTIxZTg0OTI=

from langchain_core.tools import tool
from langchain_core.messages import AIMessage
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.types import Send
from langgraph.prebuilt import ToolNode

from app.core.state import SQLMessageState, SQLValidationResult
from app.core.llms import get_default_model


# 统一的验证状态类
class ParallelValidationState(MessagesState):
    """并行SQL验证状态 - 统一状态管理"""
    # 输入数据
    sql_query: Annotated[str, lambda x, y: y or x]
    schema_info: Annotated[Dict[str, Any], lambda x, y: y or x]
    db_type: Annotated[str, lambda x, y: y or x]

    # 工作节点特定字段（可选）
    validation_type: Annotated[str, lambda x, y: y or x]  # "syntax", "security", "performance"

    # 并行验证结果
    validation_results: Annotated[List[Dict[str, Any]], operator.add]

    # 综合结果
    final_validation: Annotated[Dict[str, Any], lambda x, y: y or x]
    is_valid: Annotated[bool, lambda x, y: y if y is not None else x]

    # 错误和建议
    errors: Annotated[List[str], operator.add]
    warnings: Annotated[List[str], operator.add]
    suggestions: Annotated[List[str], operator.add]


# 保留原有的工具函数
@tool
def validate_sql_syntax(sql_query: str, db_type: str = "mysql") -> Dict[str, Any]:
    """验证SQL语法正确性"""
    try:
        errors = []
        warnings = []
        
        # 使用sqlparse进行基础语法检查
        try:
            parsed = sqlparse.parse(sql_query)
            if not parsed:
                errors.append("SQL语句无法解析")
        except Exception as e:
            errors.append(f"SQL语法错误: {str(e)}")
        
        # 检查常见的SQL问题
        sql_upper = sql_query.upper()
        
        # 检查是否包含危险操作
        dangerous_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'CREATE', 'TRUNCATE']
        for keyword in dangerous_keywords:
            if keyword in sql_upper:
                errors.append(f"包含危险操作: {keyword}")
        
        # 检查是否有SELECT语句
        if 'SELECT' not in sql_upper:
            errors.append("缺少SELECT语句")
        
        # 检查括号匹配
        if sql_query.count('(') != sql_query.count(')'):
            errors.append("括号不匹配")
        
        # 检查引号匹配
        single_quotes = sql_query.count("'")
        double_quotes = sql_query.count('"')
        if single_quotes % 2 != 0:
            warnings.append("单引号可能不匹配")
        if double_quotes % 2 != 0:
            warnings.append("双引号可能不匹配")
        
        # 检查是否有LIMIT子句（推荐）
        if 'LIMIT' not in sql_upper and 'TOP' not in sql_upper:
            warnings.append("建议添加LIMIT子句以限制结果集大小")
        
        return {
            "success": True,
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "validation_type": "syntax"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "validation_type": "syntax"
        }


@tool
def validate_sql_security(sql_query: str) -> Dict[str, Any]:
    """验证SQL安全性，检查SQL注入风险"""
    try:
        security_issues = []
        warnings = []
        
        # 检查SQL注入模式
        injection_patterns = [
            r"';.*--",  # 注释注入
            r"union.*select",  # UNION注入
            r"or.*1=1",  # 逻辑注入
            r"and.*1=1",  # 逻辑注入
            r"exec\s*\(",  # 执行函数
            r"sp_",  # 存储过程
            r"xp_",  # 扩展存储过程
        ]
        
        sql_lower = sql_query.lower()
        for pattern in injection_patterns:
            if re.search(pattern, sql_lower):
                security_issues.append(f"检测到潜在的SQL注入模式: {pattern}")
        
        # 检查动态SQL构造
        if "concat" in sql_lower or "||" in sql_query:
            warnings.append("检测到字符串拼接，请确保输入已正确转义")
        
        # 检查用户输入直接嵌入
        if "'" in sql_query and not re.search(r"'[^']*'", sql_query):
            warnings.append("检测到可能的未转义用户输入")
        
        return {
            "success": True,
            "is_secure": len(security_issues) == 0,
            "security_issues": security_issues,
            "warnings": warnings,
            "validation_type": "security"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "validation_type": "security"
        }


@tool
def validate_sql_performance(sql_query: str, schema_info: Dict[str, Any] = None) -> Dict[str, Any]:
    """验证SQL性能，识别潜在的性能问题"""
    try:
        performance_issues = []
        suggestions = []
# pylint: disable  MS80OmFIVnBZMlhucUx2b2pZbmt1cm82UW5CT053PT06ZTIxZTg0OTI=
        
        sql_upper = sql_query.upper()
        
        # 检查是否使用SELECT *
        if re.search(r'SELECT\s+\*', sql_upper):
            performance_issues.append("使用SELECT *可能影响性能，建议明确指定需要的列")
        
        # 检查是否有WHERE子句
        if 'WHERE' not in sql_upper and 'LIMIT' not in sql_upper:
            performance_issues.append("缺少WHERE子句可能导致全表扫描")
        
        # 检查JOIN类型
        if 'CROSS JOIN' in sql_upper:
            performance_issues.append("CROSS JOIN可能产生笛卡尔积，影响性能")
# noqa  Mi80OmFIVnBZMlhucUx2b2pZbmt1cm82UW5CT053PT06ZTIxZTg0OTI=
        
        # 检查子查询
        subquery_count = sql_query.count('(SELECT')
        if subquery_count > 2:
            suggestions.append(f"检测到{subquery_count}个子查询，考虑使用JOIN优化")
        
        # 检查ORDER BY
        if 'ORDER BY' in sql_upper and 'LIMIT' not in sql_upper:
            suggestions.append("ORDER BY without LIMIT可能影响性能")
        
        # 检查LIKE模式
        like_patterns = re.findall(r"LIKE\s+'([^']*)'", sql_upper)
        for pattern in like_patterns:
            if pattern.startswith('%'):
                performance_issues.append(f"LIKE模式'{pattern}'以通配符开头，无法使用索引")
        
        return {
            "success": True,
            "performance_score": max(0, 100 - len(performance_issues) * 20),
            "performance_issues": performance_issues,
            "suggestions": suggestions,
            "validation_type": "performance"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "validation_type": "performance"
        }


@tool
def fix_sql_issues(sql_query: str, validation_errors: List[str]) -> Dict[str, Any]:
    """尝试修复SQL中的问题"""
    try:
        fixed_sql = sql_query
        fixes_applied = []
        
        # 修复常见问题
        for error in validation_errors:
            if "括号不匹配" in error:
                # 简单的括号修复逻辑
                open_count = fixed_sql.count('(')
                close_count = fixed_sql.count(')')
                if open_count > close_count:
                    fixed_sql += ')' * (open_count - close_count)
                    fixes_applied.append("添加缺失的右括号")
                elif close_count > open_count:
                    fixed_sql = '(' * (close_count - open_count) + fixed_sql
                    fixes_applied.append("添加缺失的左括号")
            
            elif "缺少SELECT语句" in error:
                if not fixed_sql.upper().strip().startswith('SELECT'):
                    fixed_sql = 'SELECT * FROM (' + fixed_sql + ') AS subquery'
                    fixes_applied.append("添加SELECT语句")
            
            elif "建议添加LIMIT子句" in error:
                if 'LIMIT' not in fixed_sql.upper():
                    fixed_sql += ' LIMIT 100'
                    fixes_applied.append("添加LIMIT子句")
        
        return {
            "success": True,
            "fixed_sql": fixed_sql,
            "fixes_applied": fixes_applied,
            "original_sql": sql_query
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


class ParallelSQLValidatorAgent:
    """并行SQL验证代理 - 基于LangGraph并行工作流"""

    def __init__(self):
        self.name = "sql_validator_agent"
        self.llm = get_default_model()
        self.tools = [
            validate_sql_syntax,
            validate_sql_security,
            validate_sql_performance,
            fix_sql_issues
        ]

        # 验证工具映射
        self.validation_tools = {
            "syntax": validate_sql_syntax,
            "security": validate_sql_security,
            "performance": validate_sql_performance
        }

        # 构建并行验证图
        self.graph = self._build_parallel_validation_graph()

        # 创建代理包装器以兼容supervisor
        self.agent = self.graph  # 直接使用graph作为agent
    
    def _build_parallel_validation_graph(self) -> StateGraph:
        """构建并行验证工作流图"""
        workflow = StateGraph(ParallelValidationState)
        # 添加节点
        workflow.add_node("initialize", self._initialize_node)
        workflow.add_node("validation_orchestrator", self._validation_orchestrator)
        workflow.add_node("validation_worker", self._validation_worker_node)
        workflow.add_node("validation_synthesizer", self._validation_synthesizer_node)
        workflow.add_node("fix_issues", self._fix_issues_node)
        workflow.add_node("finalize", self._finalize_node)

        # 构建工作流边
        workflow.add_edge(START, "initialize")
        workflow.add_edge("initialize", "validation_orchestrator")
        
        # 并行验证流程
        workflow.add_conditional_edges(
            "validation_orchestrator",
            self._assign_validation_workers,
            ["validation_worker"]
        )
        workflow.add_edge("validation_worker", "validation_synthesizer")

        # 条件路由：根据验证结果决定是否需要修复
        workflow.add_conditional_edges(
            "validation_synthesizer",
            self._route_after_validation,
            {
                "fix": "fix_issues",
                "finalize": "finalize"
            }
        )
        
        workflow.add_edge("fix_issues", "finalize")
        workflow.add_edge("finalize", END)
        
        return workflow.compile(name=self.name)

    def _execute_validation_tool(self, tool_function, state: ParallelValidationState) -> Dict[str, Any]:
        """执行验证工具的通用方法"""
        try:
            llm = get_default_model()
            llm_with_tools = llm.bind_tools([tool_function])
            validator_executor_node = ToolNode([tool_function], name="validator_executor")

            # 调用LLM解析参数并执行工具
            response = llm_with_tools.invoke(state["messages"])
            tool_result = validator_executor_node.invoke({"messages": [response]})
# pragma: no cover  My80OmFIVnBZMlhucUx2b2pZbmt1cm82UW5CT053PT06ZTIxZTg0OTI=

            # 从ToolMessage中提取JSON结果
            if isinstance(tool_result, dict) and 'messages' in tool_result and tool_result['messages']:
                tool_message = tool_result['messages'][-1]
                if hasattr(tool_message, 'content'):
                    import json
                    try:
                        return json.loads(tool_message.content)
                    except json.JSONDecodeError as e:
                        return {"success": False, "error": f"Failed to parse JSON: {str(e)}"}
                else:
                    return {"success": False, "error": "No content in tool message"}
            else:
                return {"success": False, "error": "No messages in tool result"}

        except Exception as e:
            return {"success": False, "error": f"Tool execution failed: {str(e)}"}

    def _initialize_node(self, state: ParallelValidationState) -> Dict[str, Any]:
        """初始化节点"""
        return {
            **state,
            "validation_results": [],
            "errors": [],
            "warnings": [],
            "suggestions": [],
            "is_valid": True,
            "final_validation": {}
        }
    
    def _validation_orchestrator(self, state: ParallelValidationState) -> Dict[str, Any]:
        """验证编排器"""
        print(f"🔄 开始并行SQL验证: {state['sql_query'][:50]}...")
        return state
    
    def _assign_validation_workers(self, state: ParallelValidationState):
        """分配验证工作节点 - 核心并行化逻辑"""
        # 检查SQL查询是否存在


        # if not state.get("sql_query"):
        #     print("⚠️ 警告: SQL查询为空，跳过验证")
        #     return []
        
        # print(f"🔍 开始并行验证，SQL: {state['sql_query'][:50]}...")

        # 创建并行验证任务
        validation_tasks = [
            {"validation_type": "syntax", "priority": "high"},
            {"validation_type": "security", "priority": "high"},
            {"validation_type": "performance", "priority": "medium"}
        ]
        
        # 使用Send API创建并行工作节点 - 传递包含SQL查询的消息，Send实现的是动态边的功能
        return [
            Send("validation_worker", {
                "messages": state["messages"],
                "validation_type": task["validation_type"]
            })
            for task in validation_tasks
        ]

    def _validation_worker_node(self, state: ParallelValidationState) -> Dict[str, Any]:
        """验证工作节点 - 执行具体的验证任务"""
        try:
            validation_type = state["validation_type"]
            print(f"  🔍 执行{validation_type}验证...")

            # 获取对应的验证工具
            tool_function = self.validation_tools.get(validation_type)
            if not tool_function:
                raise ValueError(f"未知的验证类型: {validation_type}")
            # 执行验证工具
            result = self._execute_validation_tool(tool_function, state)
            print(f"tool_function:::{tool_function}>>> ", result)
            # 添加验证类型标识
            if isinstance(result, dict):
                result["validation_type"] = validation_type
                result["worker_id"] = f"{validation_type}_worker"
            else:
                result = {
                    "success": False,
                    "error": "Invalid result format",
                    "validation_type": validation_type,
                    "worker_id": f"{validation_type}_worker"
                }

            print(f"  ✅ {validation_type}验证完成: {result.get('success', False)}")

            return {
                "validation_results": [result]
            }

        except Exception as e:
            print(f"  ❌ {validation_type}验证失败: {str(e)}")
            return {
                "validation_results": [{
                    "success": False,
                    "error": str(e),
                    "validation_type": validation_type,
                    "worker_id": f"{validation_type}_worker"
                }]
            }

    def _validation_synthesizer_node(self, state: ParallelValidationState) -> Dict[str, Any]:
        """验证结果综合器 - 聚合并行验证结果"""
        try:
            print("🔄 综合并行验证结果...")
            validation_results = state.get("validation_results", [])

            # 分类验证结果
            syntax_results = [r for r in validation_results if r.get("validation_type") == "syntax"]
            security_results = [r for r in validation_results if r.get("validation_type") == "security"]
            performance_results = [r for r in validation_results if r.get("validation_type") == "performance"]

            # 聚合错误、警告和建议
            all_errors = []
            all_warnings = []
            all_suggestions = []

            # 处理语法验证结果
            for result in syntax_results:
                if result.get("success"):
                    all_errors.extend(result.get("errors", []))
                    all_warnings.extend(result.get("warnings", []))
                else:
                    all_errors.append(f"语法验证失败: {result.get('error', 'Unknown error')}")

            # 处理安全验证结果
            for result in security_results:
                if result.get("success"):
                    all_errors.extend(result.get("security_issues", []))
                    all_warnings.extend(result.get("warnings", []))
                else:
                    all_errors.append(f"安全验证失败: {result.get('error', 'Unknown error')}")

            # 处理性能验证结果
            for result in performance_results:
                if result.get("success"):
                    all_errors.extend(result.get("performance_issues", []))
                    all_suggestions.extend(result.get("suggestions", []))
                else:
                    all_errors.append(f"性能验证失败: {result.get('error', 'Unknown error')}")

            # 判断整体验证结果
            is_valid = len(all_errors) == 0

            # 创建综合验证结果
            final_validation = {
                "is_valid": is_valid,
                "total_errors": len(all_errors),
                "total_warnings": len(all_warnings),
                "total_suggestions": len(all_suggestions),
                "syntax_valid": len([r for r in syntax_results if r.get("success") and not r.get("errors")]) > 0,
                "security_valid": len([r for r in security_results if r.get("success") and not r.get("security_issues")]) > 0,
                "performance_score": max([r.get("performance_score", 0) for r in performance_results] + [0]),
                "validation_summary": {
                    "syntax": len(syntax_results),
                    "security": len(security_results),
                    "performance": len(performance_results)
                }
            }

            print(f"📊 验证结果综合: 有效={is_valid}, 错误={len(all_errors)}, 警告={len(all_warnings)}")

            return {
                **state,
                "final_validation": final_validation,
                "is_valid": is_valid,
                "errors": all_errors,
                "warnings": all_warnings,
                "suggestions": all_suggestions
            }

        except Exception as e:
            print(f"❌ 验证结果综合失败: {str(e)}")
            return {
                **state,
                "final_validation": {"is_valid": False, "error": str(e)},
                "is_valid": False,
                "errors": [f"验证结果综合失败: {str(e)}"]
            }

    def _route_after_validation(self, state: ParallelValidationState) -> str:
        """验证后路由决策"""
        is_valid = state.get("is_valid", False)
        errors = state.get("errors", [])

        # 如果有错误且可以修复，则进入修复流程
        if not is_valid and errors:
            fixable_errors = [
                "括号不匹配", "缺少SELECT语句", "建议添加LIMIT子句"
            ]

            has_fixable_errors = any(
                any(fixable in error for fixable in fixable_errors)
                for error in errors
            )

            if has_fixable_errors:
                print("🔧 检测到可修复的错误，进入修复流程")
                return "fix"

        print("✅ 验证完成，进入最终化")
        return "finalize"

    def _fix_issues_node(self, state: ParallelValidationState) -> Dict[str, Any]:
        """问题修复节点"""
        try:
            print("🔧 开始修复SQL问题...")

            sql_query = state["sql_query"]
            errors = state.get("errors", [])

            # 调用修复工具
            fix_result = fix_sql_issues.invoke({
                "sql_query": sql_query,
                "validation_errors": errors
            })

            if fix_result.get("success"):
                fixed_sql = fix_result.get("fixed_sql", sql_query)
                fixes_applied = fix_result.get("fixes_applied", [])

                print(f"✅ SQL修复完成，应用了{len(fixes_applied)}个修复")

                # 更新状态中的SQL
                return {
                    **state,
                    "sql_query": fixed_sql,
                    "final_validation": {
                        **state.get("final_validation", {}),
                        "fixed_sql": fixed_sql,
                        "fixes_applied": fixes_applied,
                        "was_fixed": True
                    }
                }
            else:
                print(f"❌ SQL修复失败: {fix_result.get('error')}")
                return state

        except Exception as e:
            print(f"❌ 修复过程出错: {str(e)}")
            return state

    def _finalize_node(self, state: ParallelValidationState) -> Dict[str, Any]:
        """最终化节点"""
        final_validation = state.get("final_validation", {})
        is_valid = state.get("is_valid", False)

        print(f"🎯 并行SQL验证完成: 有效={is_valid}")

        # 创建最终结果
        final_result = {
            **final_validation,
            "processing_mode": "parallel",
            "validation_complete": True,
            "timestamp": "2025-10-04"
        }

        return {
            **state,
            "final_validation": final_result
        }

    async def validate_sql(self, sql_query: str, schema_info: Dict[str, Any] = None, db_type: str = "mysql") -> Dict[str, Any]:
        """并行验证SQL - 主要接口方法"""
        try:
            print(f"🚀 开始并行SQL验证: {sql_query[:50]}...")

            # 初始化状态
            initial_state = ParallelValidationState(
                sql_query=sql_query,
                schema_info=schema_info or {},
                db_type=db_type,
                validation_results=[],
                final_validation={},
                is_valid=True,
                errors=[],
                warnings=[],
                suggestions=[]
            )

            # 执行并行验证工作流
            result = await self.graph.ainvoke(initial_state)

            # 提取最终结果
            final_validation = result.get("final_validation", {})

            return {
                "success": True,
                "is_valid": result.get("is_valid", False),
                "sql_query": result.get("sql_query", sql_query),
                "validation_details": final_validation,
                "errors": result.get("errors", []),
                "warnings": result.get("warnings", []),
                "suggestions": result.get("suggestions", []),
                "processing_mode": "parallel",
                "validation_results": result.get("validation_results", [])
            }

        except Exception as e:
            print(f"❌ 并行SQL验证失败: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "is_valid": False,
                "processing_mode": "parallel"
            }

    async def process(self, state: SQLMessageState) -> Dict[str, Any]:
        """处理SQL验证任务 - 兼容原有接口"""
        try:
            # 获取生成的SQL
            sql_query = state.get("generated_sql")
            if not sql_query:
                raise ValueError("没有找到需要验证的SQL语句")

            schema_info = state.get("schema_info", {})

            # 调用并行验证
            validation_result = await self.validate_sql(sql_query, schema_info)

            # 创建兼容的验证结果对象
            sql_validation_result = SQLValidationResult(
                is_valid=validation_result.get("is_valid", False),
                errors=validation_result.get("errors", []),
                warnings=validation_result.get("warnings", []),
                suggestions=validation_result.get("suggestions", [])
            )

            # 更新状态
            state["validation_result"] = sql_validation_result
            if sql_validation_result.is_valid:
                state["current_stage"] = "sql_execution"
            else:
                state["current_stage"] = "error_recovery"

            # 保存代理消息
            state["agent_messages"]["sql_validator"] = {
                "messages": [AIMessage(content=f"并行SQL验证完成: 有效={sql_validation_result.is_valid}")],
                "validation_details": validation_result.get("validation_details", {}),
                "processing_mode": "parallel"
            }

            return {
                "messages": [AIMessage(content=f"并行SQL验证完成: 有效={sql_validation_result.is_valid}")],
                "validation_result": sql_validation_result,
                "current_stage": state["current_stage"]
            }

        except Exception as e:
            # 记录错误
            error_info = {
                "stage": "sql_validation",
                "error": str(e),
                "retry_count": state.get("retry_count", 0),
                "processing_mode": "parallel"
            }

            state["error_history"].append(error_info)
            state["current_stage"] = "error_recovery"

            return {
                "messages": [AIMessage(content=f"并行SQL验证失败: {str(e)}")],
                "current_stage": "error_recovery"
            }


# 便捷函数
def create_parallel_sql_validator() -> ParallelSQLValidatorAgent:
    """创建并行SQL验证代理实例"""
    return ParallelSQLValidatorAgent()

async def validate_sql_parallel(sql_query: str, schema_info: Dict[str, Any] = None, db_type: str = "mysql") -> Dict[str, Any]:
    """并行验证SQL的便捷函数"""
    validator = create_parallel_sql_validator()
    return await validator.validate_sql(sql_query, schema_info, db_type)

# 创建全局实例
parallel_sql_validator_agent = ParallelSQLValidatorAgent()


if __name__ == "__main__":
    import asyncio

    async def test_parallel_validation():
        """测试并行验证功能"""
        print("🧪 测试并行SQL验证...")

        # 测试SQL
        test_sql = "SELECT * FROM users WHERE id = 1"

        # 创建验证器
        validator = create_parallel_sql_validator()

        # 执行并行验证
        result = await validator.validate_sql(test_sql)

        print(f"验证结果: {result}")
        print(f"是否有效: {result.get('is_valid')}")
        print(f"错误数量: {len(result.get('errors', []))}")
        print(f"警告数量: {len(result.get('warnings', []))}")
        print(f"建议数量: {len(result.get('suggestions', []))}")

        print("\n🎉 并行SQL验证测试完成！")

    # 运行测试
    asyncio.run(test_parallel_validation())
