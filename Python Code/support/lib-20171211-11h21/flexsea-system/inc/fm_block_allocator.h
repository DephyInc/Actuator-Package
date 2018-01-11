/****************************************************************************
	[Project] FlexSEA: Flexible & Scalable Electronics Architecture
	[Sub-project] 'flexsea-manage' Mid-level computing, and networking
	Copyright (C) 2016 Dephy, Inc. <http://dephy.com/>

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
*****************************************************************************
	[Lead developper] Jean-Francois (JF) Duval, jfduval at dephy dot com.
	[Origin] Based on Jean-Francois Duval's work at the MIT Media Lab
	Biomechatronics research group <http://biomech.media.mit.edu/>
	[Contributors]
*****************************************************************************
	[This file] fm_block_allocator: Fixed sized block allocator
*****************************************************************************
	[Change log] (Convention: YYYY-MM-DD | author | comment)
	* 2017-01-20 | igutekunst | Initial implementation
	*
*****************************************************************************/

#ifndef FM_BLOCK_ALLOCATOR_H
#define FM_BLOCK_ALLOCATOR_H

#ifdef __cplusplus
extern "C" {
#endif

typedef unsigned int size_t;

#define FM_BLOCK_SIZE 256
#define FM_NUM_BLOCKS 20

/**
 * Initialize the memory pool. Must be called before
 * calling fm_pool_allocate_block or fm_pool_free_block.
 *
 * Allocates FM_NUM_BLOCKS blocks of size FM_BLOCK_SIZE
 */
void fm_pool_init();


/**
 * Allocate and return void* to a block of
 * memory of size FM_BLOCK_SIZE, if there are
 * remaining blocks in the pool.
 *
 * You must call fm_pool_init() before using this.
 *
 * @return void* to block of memory, or NULL
 * if no space is left.
 */
void* fm_pool_allocate_block(void);

/**
 * Free a block, returning it to the pool.
 * @param block must be a poitner returned from
 * fm_pool_allocate_block, or bad things will happen.
 *
 * @return 0 on success, -1 on failure
 */
int fm_pool_free_block(void* block);


/*
 * Private message queue structure, exposed only to
 * allow easy static allocation
 *
 */
typedef struct {
	void* head;
	void* tail;
	int max_size;
	int size;
} MsgQueue ;

extern MsgQueue slave_queue;

/**
 * Initialize a MsgQueue object, able to hold up
 * to max_size items
 *
 * This queue only support pushing blocks allocated
 * from fm_pool_allocate_block
 *
 * @param q pointer to MsgQueue object to initialize
 */
int fm_queue_init(MsgQueue* q, size_t max_size);


/**
 * Put an item into a previously initialized queue.
 *
 * @param q previously initialized MsgQueue
 * @param item Block allocated from fm_pool_allocate_block
 *
 */
int fm_queue_put(MsgQueue* q, void* item);


/**
 * Get an item from the queue, or return NULL if
 * the queue is empty.
 *
 * Please free the item when done with
 * fm_pool_free_block
 *
 * @param q previously initialized MsgQueue
 * @return item (memory block) previuolsy put on the queue.
 */
void* fm_queue_get(MsgQueue* q );

int fm_queue_put_tail(MsgQueue* q, void * item);

/**
 * Helper struct to use with the MsgQueue and pool allocator
 * if you want to send sized data.
 *
 * Example
 * -------
 * BlockWrapper* b = (BlocKWrapper*) fm_pool_allocate_block();
 * b->bytes_written = sprintf(&b->data, "Hello");
 * fm_queue_put(&q, b);
 *
 *
 */

typedef struct {
	size_t bytes_written;
	char data[];
} BlockWrapper;

#define ATOMIC_BEGIN()
#define ATOMIC_END()

#ifdef __cplusplus
}
#endif

#endif //FM_BLOCK_ALLOCATOR_H

