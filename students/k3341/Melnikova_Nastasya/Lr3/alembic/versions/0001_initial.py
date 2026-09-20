"""initial TimeFlow tables"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "0001_initial"
down_revision: str | None = None
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    status_enum = sa.Enum("planned", "in_progress", "completed", name="taskstatus")
    priority_enum = sa.Enum("low", "medium", "high", name="taskpriority")
    op.create_table("users", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("email", sa.String(320), nullable=False), sa.Column("username", sa.String(50), nullable=False), sa.Column("hashed_password", sa.String(255), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.UniqueConstraint("email"), sa.UniqueConstraint("username"))
    op.create_index("ix_users_email", "users", ["email"]); op.create_index("ix_users_username", "users", ["username"])
    op.create_table("projects", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("name", sa.String(100), nullable=False), sa.Column("description", sa.Text()), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.UniqueConstraint("user_id", "name", name="uq_project_owner_name"))
    op.create_index("ix_projects_user_id", "projects", ["user_id"])
    op.create_table("tags", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("name", sa.String(50), nullable=False), sa.UniqueConstraint("user_id", "name", name="uq_tag_owner_name"))
    op.create_index("ix_tags_user_id", "tags", ["user_id"])
    op.create_table("tasks", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("project_id", sa.Integer(), sa.ForeignKey("projects.id", ondelete="SET NULL")), sa.Column("title", sa.String(200), nullable=False), sa.Column("description", sa.Text()), sa.Column("status", status_enum, nullable=False), sa.Column("priority", priority_enum, nullable=False), sa.Column("deadline", sa.DateTime(timezone=True)), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_tasks_user_id", "tasks", ["user_id"]); op.create_index("ix_tasks_project_id", "tasks", ["project_id"])
    op.create_table("task_tags", sa.Column("task_id", sa.Integer(), sa.ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True), sa.Column("tag_id", sa.Integer(), sa.ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True), sa.Column("added_at", sa.DateTime(timezone=True), nullable=False))
    op.create_table("time_entries", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("task_id", sa.Integer(), sa.ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False), sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("started_at", sa.DateTime(timezone=True), nullable=False), sa.Column("ended_at", sa.DateTime(timezone=True), nullable=False), sa.Column("duration_minutes", sa.Integer(), nullable=False))
    op.create_index("ix_time_entries_task_id", "time_entries", ["task_id"]); op.create_index("ix_time_entries_user_id", "time_entries", ["user_id"])


def downgrade() -> None:
    op.drop_table("time_entries"); op.drop_table("task_tags"); op.drop_table("tasks"); op.drop_table("tags"); op.drop_table("projects"); op.drop_table("users")
    sa.Enum(name="taskpriority").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="taskstatus").drop(op.get_bind(), checkfirst=True)

