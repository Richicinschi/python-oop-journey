#!/usr/bin/env python3
"""
Curriculum ingestion from python-oop-journey-v2 repository.

Parses the repo structure and creates a normalized manifest for the web platform.
"""
import argparse
import json
import re
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Problem:
    """A single exercise/problem."""
    slug: str
    title: str
    topic: str
    difficulty: str
    order: int
    week_slug: str
    day_slug: str
    instructions: str = ""
    starter_code: str = ""
    solution_code: str = ""
    test_code: str = ""
    hints: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Day:
    """A day of learning content."""
    slug: str
    title: str
    order: int
    week_slug: str
    theory_path: Optional[str] = None
    theory_content: str = ""
    learning_objectives: List[str] = field(default_factory=list)
    problems: List[Problem] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            **asdict(self),
            'problems': [p.to_dict() for p in self.problems]
        }


@dataclass
class Project:
    """Weekly project."""
    slug: str
    title: str
    description: str = ""
    starter_path: Optional[str] = None
    solution_path: Optional[str] = None
    test_path: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Week:
    """A week of the curriculum."""
    slug: str
    title: str
    order: int
    objective: str = ""
    prerequisites: List[str] = field(default_factory=list)
    days: List[Day] = field(default_factory=list)
    project: Optional[Project] = None
    
    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        result['days'] = [d.to_dict() for d in self.days]
        if self.project:
            result['project'] = self.project.to_dict()
        return result


@dataclass
class Curriculum:
    """Complete curriculum manifest."""
    version: str = "2.0.0"
    weeks: List[Week] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'version': self.version,
            'weeks': [w.to_dict() for w in self.weeks]
        }


class CurriculumIngestor:
    """Ingests curriculum from repository structure."""
    
    def __init__(self, source_path: Path):
        self.source_path = Path(source_path)
        self.curriculum = Curriculum()
    
    def ingest(self) -> Curriculum:
        """Parse the entire curriculum."""
        logger.info(f"Ingesting curriculum from {self.source_path}")
        
        # Find all week directories
        week_dirs = sorted([
            d for d in self.source_path.iterdir()
            if d.is_dir() and d.name.startswith('week')
        ], key=lambda d: self._extract_week_number(d.name))
        
        for week_dir in week_dirs:
            week = self._parse_week(week_dir)
            if week:
                self.curriculum.weeks.append(week)
                logger.info(f"Parsed {week.slug}: {len(week.days)} days, {sum(len(d.problems) for d in week.days)} problems")
        
        logger.info(f"Ingestion complete: {len(self.curriculum.weeks)} weeks")
        return self.curriculum
    
    def _extract_week_number(self, name: str) -> int:
        """Extract week number from directory name."""
        match = re.search(r'week(\d+)', name)
        return int(match.group(1)) if match else 999
    
    def _parse_week(self, week_dir: Path) -> Optional[Week]:
        """Parse a single week directory."""
        # Read week README for metadata
        readme_path = week_dir / "README.md"
        if not readme_path.exists():
            logger.warning(f"No README.md found in {week_dir}")
            return None
        
        readme_content = readme_path.read_text(encoding='utf-8')
        
        # Extract title and objective from README
        title = self._extract_title(readme_content) or week_dir.name.replace('_', ' ').title()
        objective = self._extract_objective(readme_content) or ""
        
        week = Week(
            slug=week_dir.name,
            title=title,
            order=self._extract_week_number(week_dir.name),
            objective=objective
        )
        
        # Parse days
        week.days = self._parse_days(week_dir, week.slug)
        
        # Parse project
        week.project = self._parse_project(week_dir)
        
        return week
    
    def _parse_days(self, week_dir: Path, week_slug: str) -> List[Day]:
        """Parse day directories or markdown files."""
        days = []
        
        # Look for day markdown files (day01_topic.md, day02_topic.md, etc.)
        day_files = sorted([
            f for f in week_dir.glob("day*.md")
            if re.match(r'day\d+_', f.name)
        ], key=lambda f: self._extract_day_number(f.name))
        
        for day_file in day_files:
            day = self._parse_day_file(day_file, week_slug)
            if day:
                days.append(day)
        
        return days
    
    def _parse_day_file(self, day_file: Path, week_slug: str) -> Optional[Day]:
        """Parse a single day markdown file."""
        content = day_file.read_text(encoding='utf-8')
        
        # Extract day number and title
        day_num = self._extract_day_number(day_file.name)
        title = self._extract_title(content) or day_file.stem.replace('_', ' ').title()
        
        day = Day(
            slug=day_file.stem,
            title=title,
            order=day_num,
            week_slug=week_slug,
            theory_path=str(day_file.relative_to(self.source_path)),
            theory_content=content
        )
        
        # Parse learning objectives from content
        day.learning_objectives = self._extract_learning_objectives(content)
        
        # Parse problems for this day
        day.problems = self._parse_problems(day_file.parent, week_slug, day.slug, day_num)
        
        return day
    
    def _parse_problems(self, week_dir: Path, week_slug: str, day_slug: str, day_num: int) -> List[Problem]:
        """Parse problems for a specific day."""
        problems = []
        
        # Look for exercises directory
        exercises_dir = week_dir / "exercises" / f"day{day_num:02d}"
        solutions_dir = week_dir / "solutions" / f"day{day_num:02d}"
        tests_dir = week_dir / "tests" / f"day{day_num:02d}"
        
        if not exercises_dir.exists():
            return problems
        
        # Find all problem files
        problem_files = sorted([
            f for f in exercises_dir.glob("problem_*.py")
        ], key=lambda f: self._extract_problem_number(f.name))
        
        for i, problem_file in enumerate(problem_files, 1):
            problem = self._parse_problem(
                problem_file, solutions_dir, tests_dir,
                week_slug, day_slug, i
            )
            if problem:
                problems.append(problem)
        
        return problems
    
    def _parse_problem(self, problem_file: Path, solutions_dir: Path, 
                       tests_dir: Path, week_slug: str, day_slug: str, 
                       order: int) -> Optional[Problem]:
        """Parse a single problem."""
        content = problem_file.read_text(encoding='utf-8')
        
        # Extract metadata from docstring
        title = self._extract_problem_title(content) or problem_file.stem
        topic = self._extract_topic(content) or ""
        difficulty = self._extract_difficulty(content) or "Medium"
        
        problem = Problem(
            slug=problem_file.stem,
            title=title,
            topic=topic,
            difficulty=difficulty,
            order=order,
            week_slug=week_slug,
            day_slug=day_slug,
            instructions=self._extract_instructions(content),
            starter_code=content,
            hints=self._extract_hints(content)
        )
        
        # Load solution if exists
        solution_file = solutions_dir / problem_file.name
        if solution_file.exists():
            problem.solution_code = solution_file.read_text(encoding='utf-8')
        
        # Load tests if exists
        test_file = tests_dir / f"test_{problem_file.name}"
        if test_file.exists():
            problem.test_code = test_file.read_text(encoding='utf-8')
        
        return problem
    
    def _parse_project(self, week_dir: Path) -> Optional[Project]:
        """Parse weekly project if exists."""
        project_dir = week_dir / "project"
        if not project_dir.exists():
            return None
        
        readme = project_dir / "README.md"
        if not readme.exists():
            return None
        
        return Project(
            slug=f"{week_dir.name}_project",
            title=self._extract_title(readme.read_text(encoding='utf-8')) or "Weekly Project",
            description=readme.read_text(encoding='utf-8')[:500],
            starter_path=str((project_dir / "starter").relative_to(self.source_path)) if (project_dir / "starter").exists() else None,
            solution_path=str((project_dir / "reference_solution").relative_to(self.source_path)) if (project_dir / "reference_solution").exists() else None,
            test_path=str((project_dir / "tests").relative_to(self.source_path)) if (project_dir / "tests").exists() else None
        )
    
    # Helper extraction methods
    def _extract_title(self, content: str) -> Optional[str]:
        """Extract title from markdown h1."""
        match = re.search(r'^# (.+)$', content, re.MULTILINE)
        return match.group(1).strip() if match else None
    
    def _extract_objective(self, content: str) -> str:
        """Extract week objective from README."""
        # Look for "Week Objective" or "Objective" section
        match = re.search(r'## Week Objective\s*\n\n([^#]+)', content)
        if match:
            return match.group(1).strip()[:200]
        return ""
    
    def _extract_day_number(self, name: str) -> int:
        """Extract day number from filename."""
        match = re.search(r'day(\d+)', name)
        return int(match.group(1)) if match else 0
    
    def _extract_problem_number(self, name: str) -> int:
        """Extract problem number from filename."""
        match = re.search(r'problem_(\d+)', name)
        return int(match.group(1)) if match else 999
    
    def _extract_learning_objectives(self, content: str) -> List[str]:
        """Extract learning objectives from day content."""
        objectives = []
        match = re.search(r'## Learning Objectives\s*\n\n((?:- .+\n)+)', content)
        if match:
            objectives = [line[2:].strip() for line in match.group(1).strip().split('\n') if line.startswith('- ')]
        return objectives
    
    def _extract_problem_title(self, content: str) -> Optional[str]:
        """Extract problem title from docstring."""
        match = re.search(r'^\s*"""\s*(.+?)\s*(?:\n|""")', content, re.DOTALL)
        if match:
            first_line = match.group(1).split('\n')[0].strip()
            return first_line if first_line else None
        return None
    
    def _extract_topic(self, content: str) -> Optional[str]:
        """Extract topic tag from problem."""
        match = re.search(r'Topic:\s*(.+?)(?:\n|$)', content, re.IGNORECASE)
        return match.group(1).strip() if match else None
    
    def _extract_difficulty(self, content: str) -> Optional[str]:
        """Extract difficulty from problem."""
        match = re.search(r'Difficulty:\s*(Easy|Medium|Hard)', content, re.IGNORECASE)
        return match.group(1).capitalize() if match else None
    
    def _extract_instructions(self, content: str) -> str:
        """Extract problem instructions from docstring."""
        match = re.search(r'^\s*"""\s*(.+?)\s*"""', content, re.DOTALL)
        return match.group(1).strip() if match else ""
    
    def _extract_hints(self, content: str) -> List[str]:
        """Extract hints from problem."""
        hints = []
        match = re.search(r'Hints?:\s*\n((?:- .+\n?)+)', content, re.IGNORECASE)
        if match:
            hints = [line[2:].strip() for line in match.group(1).strip().split('\n') if line.startswith('- ')]
        return hints


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Ingest curriculum from repository")
    parser.add_argument("--source", required=True, help="Path to python-oop-journey-v2 repository")
    parser.add_argument("--output", required=True, help="Output path for curriculum.json")
    parser.add_argument("--watch", action="store_true", help="Watch for changes (not implemented)")
    
    args = parser.parse_args()
    
    # Run ingestion
    ingestor = CurriculumIngestor(Path(args.source))
    curriculum = ingestor.ingest()
    
    # Write output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(curriculum.to_dict(), f, indent=2, ensure_ascii=False)
    
    logger.info(f"Curriculum manifest written to {output_path}")


if __name__ == "__main__":
    main()
