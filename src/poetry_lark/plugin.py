"""Poetry plugin for Lark standalone tool."""

from functools import partial
from typing import TYPE_CHECKING, List

from cleo.events.console_events import COMMAND
from poetry.console.commands.build import BuildCommand
from poetry.plugins.application_plugin import ApplicationPlugin

if TYPE_CHECKING:
    from cleo.events.console_command_event import ConsoleCommandEvent
    from cleo.events.event_dispatcher import EventDispatcher
    from poetry.console.application import Application
    from poetry.console.commands.command import Command

from poetry_lark.commands.lark.add import LarkStandaloneAdd
from poetry_lark.commands.lark.build import LarkStandaloneBuild
from poetry_lark.commands.lark.remove import LarkStandaloneRemove


class LarkStandalonePlugin(ApplicationPlugin):
    """Plugin for integrating Lark standalone commands into Poetry."""

    @property
    def commands(self) -> List['Command']:
        """List of commands provided by the plugin."""
        return [
            LarkStandaloneBuild,
            LarkStandaloneAdd,
            LarkStandaloneRemove,
        ]

    def create_builder(self, application: 'Application') -> LarkStandaloneBuild:
        """Create a builder."""
        builder = LarkStandaloneBuild(ignore_manual=True)
        builder.set_application(application)

        return builder

    def activate(self, application: 'Application') -> None:
        """Activate the plugin, registering commands and event handlers."""
        application.event_dispatcher.add_listener(
            COMMAND, partial(self.handle, application=application),
        )
        super().activate(application)

    def handle(self, event: 'ConsoleCommandEvent',
               event_name: str, dispatcher: 'EventDispatcher',
               application: 'Application') -> None:
        """
        Handle console command events and build all relevant packages.

        Arguments:
            event: The console command event.
            event_name: The name of the event being handled.
            dispatcher: The event dispatcher.
            application: The console application.

        Raises:
            ValueError: If validation fails.
        """
        if not isinstance(event.command, BuildCommand):
            return

        builder = self.create_builder(application)
        if builder.handle() != 0:
            event.stop_propagation()
