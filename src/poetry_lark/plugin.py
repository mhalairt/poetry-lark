"""Poetry plugin for Lark standalone tool."""

from cleo.events.console_command_event import ConsoleCommandEvent
from cleo.events.console_events import COMMAND
from cleo.events.event_dispatcher import EventDispatcher
from poetry.console.application import Application
from poetry.console.commands.build import BuildCommand
from poetry.console.commands.command import Command
from poetry.plugins.application_plugin import ApplicationPlugin

from typing import List

from poetry_lark.commands.build import LarkStandaloneBuild
from poetry_lark.commands.add import LarkStandaloneAdd
from poetry_lark.commands.remove import LarkStandaloneRemove


class LarkStandalonePlugin(ApplicationPlugin):
    """Plugin for integrating Lark standalone commands into Poetry."""

    @property
    def commands(self) -> List[Command]:
        """List of commands provided by the plugin."""
        return [
            LarkStandaloneBuild,
            LarkStandaloneAdd,
            LarkStandaloneRemove,
        ]

    @property
    def builder(self) -> LarkStandaloneBuild:
        """The bulder command."""
        return LarkStandaloneBuild(ignore_manual=True)

    def activate(self, application: Application) -> None:
        """Activate the plugin, registering commands and event handlers."""
        application.event_dispatcher.add_listener(COMMAND, self.handle)
        super().activate(application)

    def handle(self, event: ConsoleCommandEvent,
               event_name: str, dispatcher: EventDispatcher) -> None:
        """
        Handle console command events and build all relevant packages.

        Arguments:
            event: The console command event.
            event_name: The name of the event being handled.
            dispatcher: The event dispatcher.

        Raises:
            ValueError: If validation fails.
        """
        if not isinstance(event.command, BuildCommand):
            return

        if self.builder.handle() != 0:
            event.stop_propagation()
