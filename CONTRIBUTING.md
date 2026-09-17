# Contributing to WBY HTML PPT

Thank you for improving the Skill.

## Good contributions

- Reusable presentation controls or accessibility improvements.
- Clearer authoring, visual-direction, copywriting, or delivery guidance.
- Tests for the deck CLI or standalone HTML builder.
- Example decks that use fictional or publishable material and clearly label mockups.

## Before opening a pull request

1. Open an issue first for a substantial change so the intended outcome is clear.
2. Keep the change focused and preserve the current behavior unless the issue says otherwise.
3. Run the relevant checks:

   ```sh
   python3 tests/test_build.py
   python3 tests/test_deck.py
   ```

4. For visual or player changes, open the generated standalone HTML in a browser and verify keyboard navigation, fullscreen, overview, and reduced-motion behavior.

## Pull request notes

State what changed, why, and how you verified it. Do not include private documents, credentials, confidential screenshots, or copyrighted assets without permission.
