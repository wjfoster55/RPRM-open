# One BSD arithmetic attempt: E5 descent

Read `BSD_REBRIEF.md` for the outcome, then `E5_DESCENT_NOTE.md` for the complete
argument and source locators. This is a mathematical work record, not a paper or
an instruction to dispatch another agent.

The curve is E/Q: y^2=x^3-25x. All operations are exact rational group operations.
The subscript 5 labels the equation parameter, not a finite field.

Reproduce the finite checks using Python 3.10 or newer, without installing anything:

```sh
python -B e5_descent.py --output fresh_receipt.json
```

`E5_DESCENT_RECEIPT.json` is the assistant's executed development receipt.
The universal statements additionally use the proved arguments and the standard
mathematical dependencies identified in the note. Neither a PASS nor a source
hash alone is a proof of every theorem mentioned.

`context/` contains the two supplied context-update documents unchanged. The full
original uploaded packet was not altered. No historical closed example was rerun.
