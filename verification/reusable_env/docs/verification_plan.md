# RTL Verification Plan

## 1. Objective

Define a reusable verification strategy for RTL components using
pyUVM, Cocotb, and Verilator.

The verification environment should be developed before the final RTL
is available, allowing the infrastructure to be validated using simple
proof-of-concept DUTs.

## 2. Verification Environment

The proposed environment contains the following components:

- Test
- Sequence
- Sequence Item
- Driver
- DUT
- Monitor
- Reference Model
- Scoreboard
- Functional Coverage
- Waveform generation

## 3. Verification Flow

The sequence generates transactions that are applied to the DUT by the
driver.

The monitor observes the DUT inputs and outputs.

A reference model independently calculates the expected behavior.

The scoreboard compares the DUT result with the reference model result.

Functional coverage records which planned scenarios have been exercised.

Waveforms are generated for debugging and visual inspection.

## 4. Verification Architecture

    Sequence
       |
       v
     Driver
       |
       v
      DUT
       |
       v
    Monitor
       |
       +--------------------+
       |                    |
       v                    v
    Scoreboard           Coverage
       ^
       |
 Reference Model

## 5. Verification Items

Each RTL feature will be associated with one or more verification items.

Each verification item should define:

- Verification ID
- RTL feature
- Test objective
- Stimulus
- Expected behavior
- Reference model
- Checker
- Coverage goal
- Pass/fail criterion

## 6. Verification Matrix

| ID | Feature | Stimulus | Reference | Check | Coverage Goal | Status |
|----|---------|----------|-----------|-------|---------------|--------|
| TBD | TBD | TBD | TBD | TBD | TBD | Not defined |

The verification matrix will be completed when the target RTL and its
requirements are defined.

## 7. Pass/Fail Strategy

A test passes when the DUT behavior matches the expected behavior
produced by the reference model for all checked transactions.

A mismatch detected by the scoreboard causes the corresponding
verification test to fail.

## 8. Coverage Strategy

Functional coverage will be used to determine whether the scenarios
defined in the verification plan have been exercised.

Coverage goals will be defined according to the functionality and input
space of each target RTL block.

## 9. Waveform Strategy

Verilator tracing will be enabled to generate waveform files.

Waveforms will be used for:

- Debugging failures
- Inspecting DUT signal behavior
- Supporting verification analysis
- Demonstrating verification results

Waveform inspection is not the primary pass/fail mechanism. Automated
checking is performed by the scoreboard.

## 10. Proof of Concept

The current binary-to-Gray converter is used to validate the proposed
verification methodology.

The proof of concept currently demonstrates:

- pyUVM test structure
- Sequence and Driver
- Monitor
- Independent Python reference model
- Scoreboard
- Functional coverage
- Verilator simulation
- VCD waveform generation
- GTKWave visualization

## 11. Target RTL Integration

When the target RTL is defined, the reusable infrastructure will be
adapted by defining:

- DUT interface
- Transactions
- Sequences
- Reference model behavior
- Functional coverage points
- Verification matrix entries
- RTL-specific pass/fail criteria

The objective is to reuse the verification methodology and infrastructure
instead of creating the verification environment only after the RTL is
completed.
