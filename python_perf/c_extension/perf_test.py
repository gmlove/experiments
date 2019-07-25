import demo
import concurrent.futures


def execute_concurrently(num_threads, func, *parameters_list):
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        func_future = {executor.submit(func, *parameters): parameters for parameters in zip(*parameters_list)}
    for future in concurrent.futures.as_completed(func_future):
        try:
            data = future.result()
            yield data
        except Exception as exc:
            print('task(%s) generated an exception: %s' % (func_future[future], exc))


def test_concurrent_c_system(allow_thread: bool):
    import os
    func = lambda x: demo.system_allow_thread('ls -l') if allow_thread else demo.system('ls -l')
    for _ in execute_concurrently(os.cpu_count(), func, [1] * 10):
        pass


def test_concurrent_c_heavy_calc(allow_thread: bool):
    import os
    func = lambda x: demo.heavy_calculation_allow_thread() if allow_thread else demo.heavy_calculation()
    for _ in execute_concurrently(os.cpu_count(), func, [1] * 10):
        pass


if __name__ == '__main__':
    from datetime import datetime
    start = datetime.now()
    test_concurrent_c_system(False)
    print('execute c system with no allow_thread cost: {}s'.format((datetime.now() - start).total_seconds()), flush=True)
    start = datetime.now()
    test_concurrent_c_system(True)
    print('execute c system with allow_thread cost: {}s'.format((datetime.now() - start).total_seconds()), flush=True)

    start = datetime.now()
    test_concurrent_c_heavy_calc(False)
    print('execute c heavy calculation with no allow_thread cost: {}s'.format((datetime.now() - start).total_seconds()), flush=True)
    start = datetime.now()
    test_concurrent_c_heavy_calc(True)
    print('execute c heavy calculation with allow_thread cost: {}s'.format((datetime.now() - start).total_seconds()), flush=True)
