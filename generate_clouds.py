def generate_quads_commands(start=1, end=50):
  """Generates `quads` commands for a specified range of cloud numbers.

  Args:
    start: The starting cloud number.
    end: The ending cloud number.

  Returns:
    A list of generated `quads` commands.
  """

  commands = []
  for c in range(start, end + 1):
    c_padded = f"{c:02d}"
    command = f"quads --define-cloud --cloud cloud{c_padded} --description \"Cloud{c_padded} Environment\" --cloud-owner quads"
    commands.append(command)
  return commands

# Example usage:
commands = generate_quads_commands()
for command in commands:
  print(command)