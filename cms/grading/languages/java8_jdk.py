#!/usr/bin/env python3

# Contest Management System - http://cms-dev.github.io/
# Copyright © 2016-2017 Stefano Maggiolo <s.maggiolo@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Java programming language definition, using the default JDK installed
in the system.

"""

from shlex import quote as shell_quote

from cms.grading import Language


__all__ = ["Java8JDK"]


class Java8JDK(Language):
    """This defines the Java programming language, compiled and executed using
    the OpenJDK 8

    """

    USE_JAR = True

    @property
    def name(self):
        """See Language.name."""
        return "Java 8 / OpenJDK"

    @property
    def source_extensions(self):
        """See Language.source_extensions."""
        return [".java"]

    @property
    def requires_multithreading(self):
        """See Language.requires_multithreading."""
        return True

    def get_compilation_commands(self,
                                 source_filenames, executable_filename,
                                 for_evaluation=True):
        """See Language.get_compilation_commands."""
        compile_command = ["/usr/lib/jvm/java-8-openjdk-amd64/bin"] + source_filenames
        # We need to let the shell expand *.class as javac create
        # a class file for each inner class.
        if Java8JDK.USE_JAR:
            jar_command = ["/bin/sh", "-c",
                           " ".join(["jar", "cf",
                                     shell_quote(executable_filename),
                                     "*.class"])]
            return [compile_command, jar_command]
        else:
            zip_command = ["/bin/sh", "-c",
                           " ".join(["zip", "-r", "-", "*.class", ">",
                                     shell_quote(executable_filename)])]
            return [compile_command, zip_command]

    def get_evaluation_commands(
            self, executable_filename, main=None, args=None):
        """See Language.get_evaluation_commands."""
        args = args if args is not None else []
        if Java8JDK.USE_JAR:
            # executable_filename is a jar file, main is the name of
            # the main java class
	    # Suggested by Martin to be lowered by 24MB given problem limit of 1024MB
            return [["/usr/lib/jvm/java-8-openjdk-amd64/bin/java", "-Deval=true", "-Xmx1000M", "-Xss1000M",
                     "-Xbatch", "-XX:+UseSerialGC", "-XX:-TieredCompilation",
	                     "-XX:CICompilerCount=1", "-cp", executable_filename, main] + args]
        else:
            unzip_command = ["/usr/bin/unzip", executable_filename]
            command = ["/usr/lib/jvm/java-8-openjdk-amd64/bin/java", "-Deval=true", "-Xmx1000M", "-Xss1000M",
                       "-Xbatch", "-XX:+UseSerialGC", "-XX:-TieredCompilation",
	                       "-XX:CICompilerCount=1", main] + args
            return [unzip_command, command]
