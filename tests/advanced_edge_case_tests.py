#!/usr/bin/env python3
"""
Advanced edge case testing for VutriumSDK compatibility
Tests scenarios that might break in production usage
"""

import sys
import os
import json
import threading
import time
from typing import Dict, List, Any

def test_malformed_json_handling():
    """Test handling of malformed JSON data"""
    print("🔍 Testing malformed JSON handling...")
    try:
        from VutriumSDK import Util
        util = Util()
        
        malformed_cases = [
            '{"incomplete": ',  # Incomplete JSON
            '{"invalid": "value"',  # Missing closing brace
            '{"key": undefined}',  # Invalid value
            '',  # Empty string
            None,  # None type
            123,  # Wrong type
            '[]'  # Array instead of object
        ]
        
        for i, case in enumerate(malformed_cases):
            try:
                if case is None or isinstance(case, int):
                    packet = util.json_to_game_tick_packet(case)
                else:
                    packet = util.json_to_game_tick_packet(case)
                print(f"  ❌ Case {i+1} should have failed but didn't")
                return False
            except (TypeError, ValueError, json.JSONDecodeError) as e:
                print(f"  ✓ Case {i+1} properly handled: {type(e).__name__}")
        
        return True
    except Exception as e:
        print(f"  ❌ Test failed: {e}")
        return False

def test_missing_data_fields():
    """Test handling of missing required data fields"""
    print("\n🔍 Testing missing data fields...")
    try:
        from VutriumSDK import Util
        util = Util()
        
        # Test missing fields in game data
        incomplete_data = [
            {},  # Completely empty
            {"game_cars": []},  # Missing other fields
            {"game_info": {}},  # Missing car data
            {"localPlayerIndices": [0]},  # Missing names and cars
            {"game_cars": [{}]},  # Empty car data
        ]
        
        for i, data in enumerate(incomplete_data):
            try:
                packet = util.json_to_game_tick_packet(data)
                # Should handle gracefully with defaults
                print(f"  ✓ Case {i+1} handled gracefully: {packet.num_cars} cars")
            except Exception as e:
                print(f"  ❌ Case {i+1} failed: {e}")
                return False
        
        return True
    except Exception as e:
        print(f"  ❌ Test failed: {e}")
        return False

def test_type_validation():
    """Test type validation and conversion"""
    print("\n🔍 Testing type validation...")
    try:
        from VutriumSDK import ControllerState
        
        # Test controller state with wrong types
        controller = ControllerState()
        
        # Should handle type conversion gracefully
        controller.throttle = "1.5"  # String instead of float
        controller.jump = 1  # Int instead of bool
        controller.boost = "true"  # String instead of bool
        
        # Convert to dict - should handle type conversion
        data = controller.to_dict()
        
        # Check types are correct
        assert isinstance(data['throttle'], float), f"throttle should be float, got {type(data['throttle'])}"
        assert isinstance(data['jump'], bool), f"jump should be bool, got {type(data['jump'])}"
        assert isinstance(data['boost'], bool), f"boost should be bool, got {type(data['boost'])}"
        
        print("  ✓ Type validation and conversion works")
        return True
    except Exception as e:
        print(f"  ❌ Test failed: {e}")
        return False

def test_event_system_edge_cases():
    """Test edge cases in the event system"""
    print("\n🔍 Testing event system edge cases...")
    try:
        from VutriumSDK import SDK
        sdk = SDK()
        
        # Test subscribing to non-existent event
        def dummy_handler(evt):
            pass
        
        sdk.subscribe("NonExistentEvent", dummy_handler)
        print("  ✓ Subscription to non-existent event works")
        
        # Test subscribing same handler multiple times
        sdk.subscribe("TestEvent", dummy_handler)
        sdk.subscribe("TestEvent", dummy_handler)  # Duplicate
        print("  ✓ Duplicate subscription handled")
        
        # Test unsubscribing non-existent handler
        def another_handler(evt):
            pass
        
        sdk.unsubscribe("TestEvent", another_handler)  # Never subscribed
        print("  ✓ Unsubscribing non-existent handler handled")
        
        # Test event with malformed data
        try:
            sdk._dispatch_event("invalid json")
        except:
            print("  ✓ Malformed event data handled")
        
        return True
    except Exception as e:
        print(f"  ❌ Test failed: {e}")
        return False

def test_concurrent_operations():
    """Test concurrent operations and thread safety"""
    print("\n🔍 Testing concurrent operations...")
    try:
        from VutriumSDK import SDK, Util
        
        sdk = SDK()
        util = Util()
        
        results = {"success": 0, "failed": 0}
        
        def worker_thread(thread_id):
            try:
                # Each thread does multiple operations
                for i in range(5):
                    # Subscribe to events
                    sdk.subscribe(f"Event_{thread_id}_{i}", lambda x: None)
                    
                    # Create data structures
                    data = {"game_cars": [{"team": thread_id % 2}]}
                    packet = util.json_to_game_tick_packet(data)
                    
                    # Send JSON data
                    sdk.send_json({"thread": thread_id, "iteration": i})
                    
                results["success"] += 1
            except Exception as e:
                results["failed"] += 1
                print(f"    Thread {thread_id} failed: {e}")
        
        # Start multiple threads
        threads = []
        for i in range(5):
            t = threading.Thread(target=worker_thread, args=(i,))
            threads.append(t)
            t.start()
        
        # Wait for all threads to complete
        for t in threads:
            t.join()
        
        print(f"  ✓ Concurrent operations: {results['success']} succeeded, {results['failed']} failed")
        return results["failed"] == 0
        
    except Exception as e:
        print(f"  ❌ Test failed: {e}")
        return False

def test_memory_and_performance():
    """Test memory usage and performance characteristics"""
    print("\n🔍 Testing memory and performance...")
    try:
        from VutriumSDK import SDK, Util
        import gc
        
        # Test creating and destroying many objects
        for i in range(100):
            sdk = SDK()
            util = Util()
            
            # Create large data structures
            large_data = {
                "game_cars": [{"team": j % 2, "boost": j} for j in range(50)],
                "game_boosts": [{"is_active": True} for _ in range(34)],
                "localPlayerIndices": list(range(50)),
                "localPlayerNames": [f"Player_{j}" for j in range(50)]
            }
            
            packet = util.json_to_game_tick_packet(large_data)
            
            # Clean up
            del sdk, util, packet
        
        # Force garbage collection
        gc.collect()
        print("  ✓ Memory management test completed")
        
        # Performance test
        util = Util()
        start_time = time.time()
        
        for i in range(1000):
            data = {"game_cars": [{"team": 0}], "game_info": {"is_round_active": True}}
            packet = util.json_to_game_tick_packet(data)
        
        end_time = time.time()
        operations_per_second = 1000 / (end_time - start_time)
        
        print(f"  ✓ Performance: {operations_per_second:.0f} packet conversions/second")
        
        return True
    except Exception as e:
        print(f"  ❌ Test failed: {e}")
        return False

def test_exact_example_client_simulation():
    """Simulate the exact example_client.py workflow with real data"""
    print("\n🔍 Testing exact example_client.py simulation...")
    try:
        from VutriumSDK import SDK, download_latest_and_inject, Util
        
        # Step 1: Create SDK
        sdk = SDK()
        
        # State tracking (like in example_client.py)
        nexto_by_name = {}
        field_info_dict = None
        events_processed = 0
        
        def on_start(evt: dict):
            nonlocal events_processed
            events_processed += 1
            print(f"    ✓ OnGameEventStart processed: {evt}")
        
        def on_destroy(evt: dict):
            nonlocal events_processed, nexto_by_name
            nexto_by_name.clear()
            events_processed += 1
            print(f"    ✓ OnGameEventDestroyed processed: {evt}")
        
        def on_tick(evt: dict):
            nonlocal field_info_dict, events_processed
            events_processed += 1
            
            game = evt.get("gameTickPacket") or {}
            field_info_dict = field_info_dict or evt.get("fieldInfoPacket")
            
            if not game:
                return
            
            cars = game.get('game_cars', [])
            locals_i = game.get('localPlayerIndices', [])
            locals_n = game.get('localPlayerNames', [])
            
            if not cars or not locals_i:
                return
            
            # Simulate bot logic
            name = locals_n[0] if locals_n else None
            idx = locals_i[0]
            
            if name is None or idx < 0 or idx >= len(cars):
                return
            
            # Simulate controller state creation
            util = Util()
            if field_info_dict:
                fi = util.json_to_field_info_packet(field_info_dict)
            
            pkt = util.json_to_game_tick_packet(game)
            
            # Send controller input (exact format from example_client.py)
            sdk.send_json({
                "num_inputs": 1,
                "inputs": [{
                    "throttle": 1.0,
                    "steer": 0.5,
                    "pitch": -0.2,
                    "yaw": 0.3,
                    "roll": 0.1,
                    "jump": True,
                    "boost": False,
                    "handbrake": True,
                    "use_item": False
                }]
            })
        
        # Subscribe to events (exact event names from example_client.py)
        sdk.subscribe("OnGameEventStart", on_start)
        sdk.subscribe("OnGameEventDestroyed", on_destroy)
        sdk.subscribe("PlayerTickHook", on_tick)
        
        # Simulate events with realistic data
        test_events = [
            # Game start event
            {
                "type": "OnGameEventStart",
                "data": {"game_mode": "soccar", "map": "DFHStadium"}
            },
            
            # Player tick event with comprehensive data
            {
                "type": "PlayerTickHook",
                "gameTickPacket": {
                    "game_cars": [
                        {
                            "team": 0, 
                            "boost": 100, 
                            "is_demolished": False,
                            "is_super_sonic": False,
                            "has_wheel_contact": True,
                            "physics": {
                                "location": {"x": -2000, "y": 0, "z": 17},
                                "velocity": {"x": 1000, "y": 0, "z": 0},
                                "rotation": {"pitch": 0, "yaw": 0, "roll": 0}
                            }
                        }
                    ],
                    "localPlayerIndices": [0],
                    "localPlayerNames": ["TestPlayer"],
                    "game_info": {
                        "is_round_active": True,
                        "is_overtime": False,
                        "is_match_ended": False,
                        "game_time_remaining": 300.0
                    },
                    "game_ball": {
                        "physics": {
                            "location": {"x": 0, "y": 0, "z": 93},
                            "velocity": {"x": 0, "y": 0, "z": 0}
                        }
                    }
                },
                "fieldInfoPacket": {
                    "boost_pads": [
                        {"position": {"x": 0, "y": 0, "z": 0}, "is_active": True, "is_full_boost": False},
                        {"position": {"x": 3584, "y": 0, "z": 0}, "is_active": True, "is_full_boost": True}
                    ],
                    "goals": [
                        {"team_num": 0, "location": {"x": -5120, "y": 0, "z": 642}},
                        {"team_num": 1, "location": {"x": 5120, "y": 0, "z": 642}}
                    ]
                }
            },
            
            # Game destroyed event
            {
                "type": "OnGameEventDestroyed",
                "data": {"reason": "match_ended"}
            }
        ]
        
        # Process events manually (since we're not connected to actual server)
        for event in test_events:
            try:
                sdk._dispatch_event(json.dumps(event))
            except Exception as e:
                print(f"    Event processing error: {e}")
        
        print(f"  ✓ Processed {events_processed} events successfully")
        print(f"  ✓ nexto_by_name cleared: {len(nexto_by_name) == 0}")
        
        return events_processed == 3  # Should have processed all 3 events
        
    except Exception as e:
        print(f"  ❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all edge case tests"""
    print("🚀 ADVANCED EDGE CASE TESTING FOR VUTRIUMSDK")
    print("=" * 60)
    
    edge_case_tests = [
        test_malformed_json_handling,
        test_missing_data_fields,
        test_type_validation,
        test_event_system_edge_cases,
        test_concurrent_operations,
        test_memory_and_performance,
        test_exact_example_client_simulation
    ]
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(edge_case_tests, 1):
        try:
            if test():
                passed += 1
                print(f"✅ EDGE CASE TEST {i} PASSED")
            else:
                failed += 1
                print(f"❌ EDGE CASE TEST {i} FAILED")
        except Exception as e:
            failed += 1
            print(f"💥 EDGE CASE TEST {i} CRASHED: {e}")
        
        print()
    
    print("=" * 60)
    print(f"📊 EDGE CASE RESULTS: {passed} PASSED, {failed} FAILED")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)