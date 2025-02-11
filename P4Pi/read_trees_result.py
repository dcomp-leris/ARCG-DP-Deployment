from p4utils.utils.sswitch_thrift_API import SimpleSwitchThriftAPI #type: ignore
import time

controller = SimpleSwitchThriftAPI(9090)
start_time = time.time()

while True:
    if (time.time() - start_time) > 3:
        for i in range (0,6):
            print("major:", controller.register_read('trees_result_reg', i)) if i == 0 else print( f"tree {i}:",controller.register_read('trees_result_reg', i))
        
        print()
        start_time = time.time()