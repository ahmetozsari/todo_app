from datetime import datetime

def format_task(task):
    """Görevleri okunabilir formatta gösterir"""
    status = "✅" if task.completed else "❌"
    due = task.due_date.strftime("%Y-%m-%d") if task.due_date else "—"
    priority = task.priority if task.priority else "—"
    return f"[{status}] {task.id}. {task.title} | Öncelik: {priority} | Tarih: {due}"


def parse_date(date_str):
    """YYYY-MM-DD stringini datetime objesine çevirir"""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except (ValueError, TypeError):
        return None
