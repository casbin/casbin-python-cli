import casbin  
  
def test_batch_enforce():  
    try:  
        enforcer = casbin.Enforcer("examples/basic_model.conf", "examples/basic_policy.csv")  
          
        # 检查是否有batch_enforce方法  
        print(f"Has batch_enforce: {hasattr(enforcer, 'batch_enforce')}")  
          
        if hasattr(enforcer, 'batch_enforce'):  
            # 测试批量执行  
            requests = [  
                ["alice", "data1", "read"],  
                ["bob", "data2", "write"],   
                ["jack", "data3", "read"]  
            ]  
            result = enforcer.batch_enforce(requests)  
            print(f"Batch enforce result: {result}")  
            print(f"Result type: {type(result)}")  
        else:  
            print("batch_enforce method not found")  
              
    except Exception as e:  
        print(f"Error: {e}")  
        import traceback  
        traceback.print_exc()  
  
if __name__ == "__main__":  
    test_batch_enforce()