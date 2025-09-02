# [AsyncIO](https://docs.python.org/3/library/asyncio.html)

## What is AsyncIO?

AsyncIO is Python's built-in library for writing **concurrent code** using the `async`/`await` syntax. It's designed for **single-threaded**, **single-process** execution using **cooperative multitasking**.

### Key Concepts

- **Asynchronous ≠ Faster**: AsyncIO doesn't automatically make code faster. It allows doing other useful work instead of sitting idle while waiting for I/O operations.
- **I/O Bound Tasks**: AsyncIO excels at tasks that wait for external operations (network requests, database queries, file operations).
- **Cooperative Multitasking**: Tasks voluntarily give up control to allow other tasks to run.

## Core Terminology

### 1. Event Loop

- The engine that runs and manages asynchronous functions
- Keeps track of all tasks and schedules their execution
- Started with `asyncio.run(main_function())`

### 2. Coroutines

Two types to understand:

- **Coroutine Function**: Defined with `async def`
- **Coroutine Object**: The awaitable returned when calling a coroutine function

```python
async def fetch_data(param):  # Coroutine function
    await asyncio.sleep(param)
    return f"Result of {param}"

coro = fetch_data(1)  # Coroutine object
```

### 3. Tasks

- Wrappers around coroutines that are scheduled on the event loop
- Enable concurrent execution
- Created with `asyncio.create_task(coroutine)`

### 4. Awaitables

Objects that can be used with the `await` keyword. Three main types:

- Coroutines
- Tasks
- Futures (low-level, rarely used directly)

### 5. The `await` Keyword

- Can only be used inside `async` functions
- Pauses execution of current function
- Yields control back to event loop
- Resumes when awaited operation completes

## What Makes Something Awaitable?

Objects must implement a special `__await__` method to be awaitable. This is why:

- You **cannot** await `time.sleep()` - it doesn't have `__await__`
- You **cannot** await regular synchronous functions
- You **must** use `asyncio.sleep()` instead of `time.sleep()`
- Synchronous libraries don't know how to work with the event loop

## Common Patterns and Examples

### Example 1: Synchronous Code (Baseline)

```python
import time

def fetch_data(param):
    print(f"Do something with {param}...")
    time.sleep(param)
    print(f"Done with {param}")
    return f"Result of {param}"

def main():
    result1 = fetch_data(1)  # Takes 1 second
    result2 = fetch_data(2)  # Takes 2 seconds
    return [result1, result2]

# Total time: 3 seconds (sequential)
```

### Example 2: Common Mistake - Awaiting Coroutines Directly

```python
import asyncio

async def fetch_data(param):
    await asyncio.sleep(param)
    return f"Result of {param}"

async def main():
    # MISTAKE: Creating coroutine objects, not tasks
    task1 = fetch_data(1)  # Just return a coroutine object
    task2 = fetch_data(2)  # Just return a coroutine object

    result1 = await task1  # Schedules and runs to completion
    result2 = await task2  # Then schedules and runs to completion
    return [result1, result2]

# Still takes 3 seconds - no concurrency!
```

### Example 3: Correct Concurrent Execution

```python
import asyncio

async def fetch_data(param):
    await asyncio.sleep(param)
    return f"Result of {param}"

async def main():
    # CORRECT: Create tasks to schedule on event loop
    task1 = asyncio.create_task(fetch_data(1))
    task2 = asyncio.create_task(fetch_data(2))

    result1 = await task1
    result2 = await task2
    return [result1, result2]

# Takes 2 seconds (concurrent execution)
```

## Critical Mistake: Blocking the Event Loop

### What NOT to Do

```python
import asyncio
import time

async def fetch_data(param):
    print(f"Do something with {param}...")
    time.sleep(param)  # BLOCKS the event loop!
    print(f"Done with {param}")
    return f"Result of {param}"

# This defeats the purpose of async - no concurrency
```

### Why This Fails

- `time.sleep()` is synchronous and blocking
- It doesn't know how to yield control to the event loop
- Use `asyncio.sleep()` instead for async-compatible sleeping

## Running Blocking Code in AsyncIO

When you must use blocking/synchronous code that doesn't have async alternatives:

### Key Principle: Don't Run Blocking Code Directly in Async Functions

**Problem**: If you put blocking code inside an async function, it will block the entire event loop:

```python
# BAD - This blocks the event loop
async def fetch_data(param):
    print(f"Do something with {param}...")
    time.sleep(param)  # BLOCKS everything!
    print(f"Done with {param}")
    return f"Result of {param}"
```

Even when scheduled as tasks, this defeats concurrency because the blocking call prevents the event loop from switching between tasks.

### Solution 1: Using Threads with `asyncio.to_thread()`

```python
import asyncio

def fetch_data(param):  # Regular synchronous function
    print(f"Do something with {param}...", flush=True)
    time.sleep(param)  # Blocking operation is OK here
    print(f"Done with {param}", flush=True)
    return f"Result of {param}"

async def main():
    # Wrap synchronous function with asyncio.to_thread()
    task1 = asyncio.create_task(asyncio.to_thread(fetch_data, 1))
    task2 = asyncio.create_task(asyncio.to_thread(fetch_data, 2))

    result1 = await task1
    print("Thread 1 fully completed")
    result2 = await task2
    print("Thread 2 fully completed")
    return [result1, result2]
```

**Key Points about `asyncio.to_thread()`**:

- Pass the **function itself** (not executed), then arguments separately
- Wraps synchronous function with a future, making it awaitable
- Manages thread creation and cleanup automatically

### Solution 2: Using Processes with `loop.run_in_executor()`

```python
import asyncio
from concurrent.futures import ProcessPoolExecutor

async def main():
    loop = asyncio.get_running_loop()

    with ProcessPoolExecutor() as executor:
        # Pass function and arguments separately
        task1 = loop.run_in_executor(executor, fetch_data, 1)
        task2 = loop.run_in_executor(executor, fetch_data, 2)

        result1 = await task1
        print("Process 1 fully completed")
        result2 = await task2
        print("Process 2 fully completed")

    return [result1, result2]
```

**Key Points about Process Execution**:

- Requires `if __name__ == "__main__":` guard to prevent infinite loops
- Processes have more overhead than threads for startup/teardown
- Use for CPU-bound tasks or when you need true isolation

### Important Implementation Details

1. **Function Argument Passing**:

   ```python
   # CORRECT - Pass function and args separately
   asyncio.to_thread(fetch_data, 1)

   # WRONG - Don't execute the function first
   asyncio.to_thread(fetch_data(1))
   ```

2. **Print Statement Buffering**: Use `flush=True` in print statements when using threads/processes to ensure output appears in expected order.

3. **Process Pool Context Manager**: Always use ProcessPoolExecutor within a context manager to ensure proper cleanup.

### Performance Considerations

- Threads and processes add overhead for creation and destruction
- Above example took ~4 seconds total because it ran two groups sequentially:
  - 2 seconds for thread group (running concurrently)
  - 2 seconds for process group (running concurrently)
- The overhead makes total time slightly longer than pure async alternatives

## Managing Multiple Tasks

### Manual Task Management

```python
async def main():
    # Create tasks - this schedules them immediately
    task1 = asyncio.create_task(fetch_data(1))
    task2 = asyncio.create_task(fetch_data(2))

    # Await order doesn't determine execution order
    result1 = await task1
    result2 = await task2
    return [result1, result2]
```

**Key Points**:

- Tasks are scheduled immediately when created with `asyncio.create_task()`
- Both tasks start running concurrently once the event loop gets control
- Await order controls when you process results, not when tasks execute

### Understanding Await Order vs Execution Order

The transcript demonstrates this with Example 4:

```python
async def main():
    task1 = asyncio.create_task(fetch_data(1))  # Sleeps 1 second
    task2 = asyncio.create_task(fetch_data(2))  # Sleeps 2 seconds

    # Even though we await task2 first...
    result2 = await task2
    print("Task 2 fully completed")
    result1 = await task1  # This might already be done!
    print("Task 1 fully completed")
    return [result1, result2]
```

**What happens**:

- Both tasks start immediately when created
- Task 1 finishes first (1 second) but result is stored in memory
- We wait for Task 2 to complete (2 seconds) before proceeding
- When we await Task 1, it's already done - we just retrieve the stored result

**Important**: The event loop uses a FIFO (First In, First Out) queue for ready tasks. You shouldn't rely on specific execution order - let the event loop handle scheduling.

### Using `asyncio.gather()`

#### Gathering Coroutines Directly

```python
async def main():
    # Create list of coroutines (not scheduled yet)
    coroutines = [fetch_data(i) for i in range(1, 3)]

    # Gather schedules AND runs them concurrently
    results = await asyncio.gather(*coroutines, return_exceptions=True)
    print(f"Coroutine Results: {results}")
    return results
```

#### Gathering Pre-created Tasks

```python
async def main():
    # Create and schedule tasks first
    tasks = [asyncio.create_task(fetch_data(i)) for i in range(1, 3)]

    # Gather awaits all of them
    results = await asyncio.gather(*tasks)
    print(f"Task Results: {results}")
    return results
```

**Key Differences**:

- **Coroutines**: Scheduled and run when `gather()` is called
- **Tasks**: Already scheduled when created, `gather()` just waits for completion
- **Asterisk (`*`)**: Unpacks the list - `gather()` doesn't accept lists directly

#### When to Use Tasks vs Coroutines with Gather

- **Use coroutines** if you just want results
- **Use tasks** if you need to monitor or interact with tasks before completion

### Using Task Groups (Python 3.11+)

```python
async def main():
    async with asyncio.TaskGroup() as tg:
        # Create tasks within the group
        results = [tg.create_task(fetch_data(i)) for i in range(1, 3)]
        # NO await needed - context manager handles it

    # Access results after context exits
    final_results = [result.result() for result in results]
    print(f"Task Group Results: {final_results}")
    return final_results
```

**Task Group Features**:

- **Async Context Manager**: Uses `async with` for setup/teardown
- **Automatic Awaiting**: No manual await needed - happens when exiting context
- **Task Tracking**: Automatically tracks all tasks created within the group
- **Error Management**: Handles cancellations and errors for the entire group

### Alternative: Using `asyncio.sleep()` for Simple Coordination

The transcript shows you can also yield control without specific task dependencies:

```python
async def main():
    task1 = asyncio.create_task(fetch_data(1))
    task2 = asyncio.create_task(fetch_data(2))

    # Yield control for 2.5 seconds - tasks run in background
    await asyncio.sleep(2.5)

    # Tasks likely completed by now
    return "Tasks finished in background"
```

This demonstrates that `await` is about yielding control, not necessarily waiting for specific tasks.

## Error Handling: gather() vs TaskGroup

### `asyncio.gather()`

- **`return_exceptions=False`** (default): Raises first exception, other tasks continue running
- **`return_exceptions=True`**: All tasks complete, exceptions returned in results list
- Use when you want some tasks to succeed even if others fail

### `TaskGroup`

- Fails fast: cancels all tasks if any task fails
- Raises `ExceptionGroup` with all exceptions
- Use when all tasks must succeed or fail together

## Important Notes

### Event Loop Execution Order

- Tasks run in FIFO (First In, First Out) order when ready
- `await` doesn't guarantee immediate execution of that specific task
- `await` guarantees you won't proceed until the awaited task completes
- Don't rely on execution order - let the event loop manage scheduling

### Async Context Managers

```python
async with some_async_resource() as resource:
    # Async setup and teardown
    pass
```

Used for resources requiring async setup/cleanup (databases, network connections, etc.)

### Best Practices

1. Always use `asyncio.create_task()` for concurrent execution
2. Use `asyncio.sleep()` instead of `time.sleep()`
3. Use async libraries (httpx, aiohttp) instead of sync ones (requests)
4. Don't block the event loop with synchronous operations
5. Use TaskGroup for fail-together scenarios
6. Use gather with `return_exceptions=True` for independent tasks

## Common Pitfalls and Mistakes

### 1. Forgetting to Await Tasks/Coroutines

- **Problem**: Tasks appear to run but are actually canceled
- **Symptoms**:
  - No error messages thrown
  - Print statements may appear, making it seem successful
  - Tasks show as "canceled" in output
  - Code reaches start of tasks but never completes them
- **Solution**: Always use `await` when calling async functions or tasks

### 2. Script Ending Before Tasks Complete

- **Problem**: Main script finishes execution while background tasks are still running
- **Example**: Awaiting a short sleep (0.1s) while a task takes 2s to complete
- **Result**: Some tasks never finish, incomplete results
- **Solution**: Ensure all tasks are properly awaited before script termination

### 3. Using Blocking IO in Async Code

- **Problem**: Accidentally using synchronous/blocking calls within asynchronous code
- **Impact**: Defeats the purpose of async programming, blocks the event loop
- **Solution**: Use async-compatible libraries and functions

## Debugging and Development Tips

### Linting

- Use a good linter with proper AsyncIO rules configured
- Helps catch common async mistakes early in development

### Debug Mode

```python
asyncio.run(main(), debug=True)
```

- Set `debug=True` in `asyncio.run()` during development
- Helps identify issues in async code
- **Important**: Only use debug mode in development, not production

### Profiling

- Use profilers to understand where code spends time
- Helps identify bottlenecks and determine if work is IO-bound or CPU-bound

## When to Use AsyncIO vs Threads vs Multiprocessing

### AsyncIO

- **Best for**: IO-bound work that can run concurrently
- **Requirement**: Asynchronous libraries must be available
- **Examples**: Web requests, database queries, file operations (with async libraries)

### Threads

- **Best for**: IO-bound work when async libraries aren't available
- **Use case**: When you must use synchronous code for IO operations

### Multiprocessing

- **Best for**: CPU-bound work
- **Purpose**: Speed up computationally intensive tasks

## AsyncIO Ecosystem and Libraries

### Growing Library Support

- More async-compatible libraries being developed constantly
- Expanding ecosystem makes AsyncIO more practical for real projects

### Key Libraries

- **Web Frameworks**: FastAPI
- **HTTP Clients**: HTTPX, AIOHTTP
- **Databases**:
  - SQLAlchemy (now supports async)
  - Async drivers for PostgreSQL, MySQL
- **File Operations**: AIO Files

Readings:

- [Python Tutorial: AsyncIO - Complete Guide to Asynchronous Programming with Animations](https://www.youtube.com/watch?v=oAkLSJNr5zY&t=31s)
- [AsyncIO-Code-Examples](https://github.com/CoreyMSchafer/AsyncIO-Code-Examples/tree/main)
