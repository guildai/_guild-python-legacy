import os
import subprocess

import guild.main_impl

import guild.check_cmd
import guild.evaluate_cmd
import guild.prepare_cmd
import guild.project_cmd
import guild.query_cmd
import guild.runs_cmd
import guild.train_cmd

if __name__ == "__main__":
    guild.main_impl.main([
        guild.check_cmd,
        guild.evaluate_cmd,
        guild.prepare_cmd,
        guild.project_cmd,
        guild.query_cmd,
        guild.runs_cmd,
        guild.train_cmd,
    ])
